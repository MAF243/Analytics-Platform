from abc import ABC, abstractmethod

from backend.app.domain.entities.analysis_result import AnalyticsContext


class IProfilingService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class ICleaningService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IFeatureSelectionService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IScalingStrategy(ABC):
    @abstractmethod
    def scale(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IScalingService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IPCAService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IElbowStrategy(ABC):
    @abstractmethod
    def detect(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IElbowDetectionService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IClusteringService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class ISummaryService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class ICategorySummaryService(ABC):
    @abstractmethod
    def process(self, context: AnalyticsContext) -> AnalyticsContext:
        pass


class IDashboardBuilder(ABC):
    @abstractmethod
    def build(self, context: AnalyticsContext) -> AnalyticsContext:
        pass
