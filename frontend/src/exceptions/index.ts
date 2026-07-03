export class FrontendException extends Error {
  public code: string;
  constructor(message: string, code: string = 'UNKNOWN') {
    super(message);
    this.code = code;
    this.name = 'FrontendException';
  }
}

export class ApiException extends FrontendException {
  public statusCode: number;
  constructor(message: string, statusCode: number, code = 'API_ERROR') {
    super(message, code);
    this.statusCode = statusCode;
    this.name = 'ApiException';
  }
}

export class ValidationException extends ApiException {
  constructor(message: string) { super(message, 422, 'VALIDATION_ERROR'); this.name = 'ValidationException'; }
}

export class NetworkException extends FrontendException {
  constructor(message = 'Network request failed') { super(message, 'NETWORK_ERROR'); this.name = 'NetworkException'; }
}

export class TimeoutException extends FrontendException {
  constructor(message = 'Request timed out') { super(message, 'TIMEOUT_ERROR'); this.name = 'TimeoutException'; }
}

export class NotFoundException extends ApiException {
  constructor(message = 'Resource not found') { super(message, 404, 'NOT_FOUND'); this.name = 'NotFoundException'; }
}

export class UnauthorizedException extends ApiException {
  constructor(message = 'Unauthorized') { super(message, 401, 'UNAUTHORIZED'); this.name = 'UnauthorizedException'; }
}

export class ForbiddenException extends ApiException {
  constructor(message = 'Forbidden') { super(message, 403, 'FORBIDDEN'); this.name = 'ForbiddenException'; }
}

export class ConflictException extends ApiException {
  constructor(message = 'Conflict') { super(message, 409, 'CONFLICT'); this.name = 'ConflictException'; }
}
