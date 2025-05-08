import { Test, TestingModule } from '@nestjs/testing';
import { UserController } from './user.controller';
import { UserService } from './user.service';
import { CreateUserDto } from './create-user.dto';
import { User } from './user.entity';

describe('UserController', () => {
  let controller: UserController;
  let service: UserService;

  const mockUserService = {
    createUser: jest.fn(),
    findAll: jest.fn(),
    findById: jest.fn(),
    updateUser: jest.fn(),
    deleteUser: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UserController],
      providers: [{ provide: UserService, useValue: mockUserService }],
    }).compile();

    controller = module.get<UserController>(UserController);
    service = module.get<UserService>(UserService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  it('should create a user', async () => {
    const dto: CreateUserDto = {
      username: 'test',
      password: 'pass',
      role: 'user',
    };
    const user = { id: 1, ...dto } as User;
    mockUserService.createUser.mockResolvedValue(user);

    expect(await controller.create(dto)).toEqual(user);
    expect(mockUserService.createUser).toHaveBeenCalledWith(dto);
  });

  it('should return all users', async () => {
    const users = [
      { id: 1, username: 'test', password: 'pass', role: 'user' },
    ] as User[];
    mockUserService.findAll.mockResolvedValue(users);

    expect(await controller.findAll()).toEqual(users);
    expect(mockUserService.findAll).toHaveBeenCalled();
  });

  it('should return a user by id', async () => {
    const user = {
      id: 1,
      username: 'test',
      password: 'pass',
      role: 'user',
    } as User;
    mockUserService.findById.mockResolvedValue(user);

    expect(await controller.findOne(1)).toEqual(user);
    expect(mockUserService.findById).toHaveBeenCalledWith(1);
  });

  it('should update a user', async () => {
    const updatedUser = {
      id: 1,
      username: 'test',
      password: 'newpass',
      role: 'user',
    } as User;
    mockUserService.updateUser.mockResolvedValue(updatedUser);

    expect(await controller.update(1, { password: 'newpass' })).toEqual(
      updatedUser,
    );
    expect(mockUserService.updateUser).toHaveBeenCalledWith(1, {
      password: 'newpass',
    });
  });

  it('should delete a user', async () => {
    mockUserService.deleteUser.mockResolvedValue(undefined);

    expect(await controller.remove(1)).toBeUndefined();
    expect(mockUserService.deleteUser).toHaveBeenCalledWith(1);
  });
});
