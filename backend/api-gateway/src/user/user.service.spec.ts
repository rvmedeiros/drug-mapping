import { Test, TestingModule } from '@nestjs/testing';
import { UserService } from './user.service';
import { getRepositoryToken } from '@nestjs/typeorm';
import { User } from './user.entity';
import { Repository } from 'typeorm';
import { ConfigService } from '@nestjs/config';
import * as bcrypt from 'bcrypt';

describe('UserService', () => {
  let service: UserService;
  let userRepository: Repository<User>;

  const mockUserRepository = {
    findOne: jest.fn(),
    create: jest.fn(),
    save: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
  };

  const mockConfigService = {
    get: jest.fn().mockReturnValue('admin'),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: mockUserRepository,
        },
        {
          provide: ConfigService,
          useValue: mockConfigService,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    userRepository = module.get<Repository<User>>(getRepositoryToken(User));
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });

  it('should create an admin user if it does not exist', async () => {
    mockUserRepository.findOne.mockResolvedValueOnce(null);
    mockUserRepository.save.mockResolvedValueOnce(true);

    await service.onModuleInit();

    expect(mockUserRepository.create).toHaveBeenCalled();
    expect(mockUserRepository.save).toHaveBeenCalled();
    expect(mockUserRepository.findOne).toHaveBeenCalledWith({
      where: { username: 'admin' },
    });
  });
});
