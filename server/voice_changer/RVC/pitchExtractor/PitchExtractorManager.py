from typing import Protocol
from const import PitchExtractorType
from voice_changer.RVC.pitchExtractor.CrepeOnnxPitchExtractor import CrepeOnnxPitchExtractor
from voice_changer.RVC.pitchExtractor.CrepePitchExtractor import CrepePitchExtractor
from voice_changer.RVC.pitchExtractor.PitchExtractor import PitchExtractor
from voice_changer.RVC.pitchExtractor.RMVPEOnnxPitchExtractor import RMVPEOnnxPitchExtractor
from voice_changer.RVC.pitchExtractor.RMVPEPitchExtractor import RMVPEPitchExtractor
from voice_changer.RVC.pitchExtractor.FcpePitchExtractor import FcpePitchExtractor
from voice_changer.RVC.pitchExtractor.FcpeOnnxPitchExtractor import FcpeOnnxPitchExtractor
from settings import ServerSettings
import logging
logger = logging.getLogger(__name__)

class PitchExtractorManager(Protocol):
    pitch_extractor: PitchExtractor | None = None
    params: ServerSettings

    @classmethod
    def initialize(cls, params: ServerSettings):
        cls.params = params

    @classmethod
    def getPitchExtractor(cls, pitch_extractor: PitchExtractorType, force_reload: bool) -> PitchExtractor:
        cls.pitch_extractor = cls.loadPitchExtractor(pitch_extractor, force_reload)
        return cls.pitch_extractor

    @classmethod
    def loadPitchExtractor(cls, pitch_extractor: PitchExtractorType, force_reload: bool) -> PitchExtractor:
        if cls.pitch_extractor is not None \
            and pitch_extractor == cls.pitch_extractor.type \
            and not force_reload:
            logger.info('Reusing pitch extractor.')
            return cls.pitch_extractor

        logger.info(f'Loading pitch extractor {pitch_extractor}')
        try:
            if pitch_extractor == 'crepe_tiny':
                return CrepePitchExtractor(pitch_extractor, cls.params.crepe_tiny)
            elif pitch_extractor == 'crepe_full':
                return CrepePitchExtractor(pitch_extractor, cls.params.crepe_full)
            elif pitch_extractor == "crepe_tiny_onnx":
                return CrepeOnnxPitchExtractor(pitch_extractor, cls.params.crepe_onnx_tiny)
            elif pitch_extractor == "crepe_full_onnx":
                return CrepeOnnxPitchExtractor(pitch_extractor, cls.params.crepe_onnx_full)
            elif pitch_extractor == "rmvpe":
                return RMVPEPitchExtractor(cls.params.rmvpe)
            elif pitch_extractor == "rmvpe_onnx":
                return RMVPEOnnxPitchExtractor(cls.params.rmvpe_onnx)
            elif pitch_extractor == "fcpe":
                return FcpePitchExtractor(cls.params.fcpe)
            elif pitch_extractor == "fcpe_onnx":
                return FcpeOnnxPitchExtractor(cls.params.fcpe_onnx)
            else:
                logger.warn(f"PitchExctractor not found {pitch_extractor}. Fallback to rmvpe_onnx")
                return RMVPEOnnxPitchExtractor(cls.params.rmvpe_onnx)
        except RuntimeError as e:
            logger.error(f'Failed to load {pitch_extractor}. Fallback to rmvpe_onnx.')
            logger.exception(e)
            return RMVPEOnnxPitchExtractor(cls.params.rmvpe_onnx)
