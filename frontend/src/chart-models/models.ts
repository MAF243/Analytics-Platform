export interface IChartModel {
  title: string;
}

export class PieChartModel implements IChartModel {
  public title: string;
  public series: { name: string, value: number }[];
  constructor(title: string, series: { name: string, value: number }[]) {
    this.title = title;
    this.series = series;
  }
}

export class ScatterChartModel implements IChartModel {
  public title: string;
  public points: { x: number, y: number, cluster: string }[];
  constructor(title: string, points: { x: number, y: number, cluster: string }[]) {
    this.title = title;
    this.points = points;
  }
}

export class BarChartModel implements IChartModel {
  public title: string;
  public categories: string[];
  public values: number[];
  constructor(title: string, categories: string[], values: number[]) {
    this.title = title;
    this.categories = categories;
    this.values = values;
  }
}

export class StackedBarChartModel implements IChartModel {
  public title: string;
  public categories: string[]; // e.g., features
  public series: { name: string, data: number[] }[]; // e.g., cluster means
  constructor(title: string, categories: string[], series: { name: string, data: number[] }[]) {
    this.title = title;
    this.categories = categories;
    this.series = series;
  }
}

export class GaugeChartModel implements IChartModel {
  public title: string;
  public score: number;
  constructor(title: string, score: number) {
    this.title = title;
    this.score = score;
  }
}
