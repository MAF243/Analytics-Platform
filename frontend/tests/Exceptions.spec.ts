import { describe, it, expect } from 'vitest';
import { 
  ApiException, TimeoutException, NetworkException, ValidationException, 
  NotFoundException, UnauthorizedException, ForbiddenException, ConflictException 
} from '../src/exceptions';
import { BaseRepository } from '../src/repositories/BaseRepository';

describe('All Exceptions', () => {
  it('instantiates all exceptions', () => {
    expect(new TimeoutException().code).toBe('TIMEOUT_ERROR');
    expect(new NetworkException().code).toBe('NETWORK_ERROR');
    expect(new ValidationException('msg').statusCode).toBe(422);
    expect(new NotFoundException().statusCode).toBe(404);
    expect(new UnauthorizedException().statusCode).toBe(401);
    expect(new ForbiddenException().statusCode).toBe(403);
    expect(new ConflictException().statusCode).toBe(409);
  });
});

describe('BaseRepository handleAxiosError', () => {
  class TestRepo extends BaseRepository {
    public triggerError(err: any) {
      // @ts-expect-error bypass protected
      return this.handleAxiosError(err);
    }
  }

  it('throws Timeout on ECONNABORTED', () => {
    const repo = new TestRepo();
    expect(() => repo.triggerError({ code: 'ECONNABORTED' })).toThrow(TimeoutException);
  });
  it('throws NetworkException on missing response', () => {
    const repo = new TestRepo();
    expect(() => repo.triggerError({})).toThrow(NetworkException);
  });
  it('throws specific exceptions based on status', () => {
    const repo = new TestRepo();
    expect(() => repo.triggerError({ response: { status: 401 } })).toThrow(UnauthorizedException);
    expect(() => repo.triggerError({ response: { status: 403 } })).toThrow(ForbiddenException);
    expect(() => repo.triggerError({ response: { status: 404 } })).toThrow(NotFoundException);
    expect(() => repo.triggerError({ response: { status: 409 } })).toThrow(ConflictException);
    expect(() => repo.triggerError({ response: { status: 422 } })).toThrow(ValidationException);
    expect(() => repo.triggerError({ response: { status: 500 } })).toThrow(ApiException);
  });
});
