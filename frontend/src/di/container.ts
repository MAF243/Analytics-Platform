import { ConsoleLogger, type ILogger } from '../observability/logger';
import { DashboardRepository } from '../repositories/DashboardRepository';
import { UploadRepository } from '../repositories/UploadRepository';
import { AnalysisRepository } from '../repositories/AnalysisRepository';


export class DIContainer {
  private static instance: DIContainer;
  private services = new Map<string, any>();

  private constructor() {
    // Register Default Implementations
    this.register('ILogger', new ConsoleLogger());
    this.register('DashboardRepository', new DashboardRepository());
    this.register('UploadRepository', new UploadRepository());
    this.register('AnalysisRepository', new AnalysisRepository());
  }

  static getInstance(): DIContainer {
    if (!DIContainer.instance) {
      DIContainer.instance = new DIContainer();
    }
    return DIContainer.instance;
  }

  register<T>(key: string, instance: T): void {
    if (this.services.has(key)) {
      this.resolve<ILogger>('ILogger')?.warn(`Service ${key} is already registered. Overwriting.`);
    }
    this.services.set(key, instance);
  }

  resolve<T>(key: string): T {
    const service = this.services.get(key);
    if (!service) {
      throw new Error(`Service ${key} not found in DI Container`);
    }
    return service as T;
  }

  // Convenience accessors mapping to keys
  get logger(): ILogger { return this.resolve<ILogger>('ILogger'); }
  get dashboardRepository(): DashboardRepository { return this.resolve<DashboardRepository>('DashboardRepository'); }
  get uploadRepository(): UploadRepository { return this.resolve<UploadRepository>('UploadRepository'); }
  get analysisRepository(): AnalysisRepository { return this.resolve<AnalysisRepository>('AnalysisRepository'); }
}

export const container = DIContainer.getInstance();
