import { Test, TestingModule } from "@nestjs/testing";
import { UserService } from "./user.service";
import { getRepositoryToken } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import { User } from "./user.entity";

describe("UserService", () => {
  let service: UserService;
  let repo: Repository<User>;

  const mockUserRepository = {
    create: jest.fn(),
    save: jest.fn(),
    findOne: jest.fn(),
  };

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UserService,
        {
          provide: getRepositoryToken(User),
          useValue: mockUserRepository,
        },
      ],
    }).compile();

    service = module.get<UserService>(UserService);
    repo = module.get<Repository<User>>(getRepositoryToken(User));
  });

  it("should create a new user", async () => {
    const userDto = { username: "test", password: "1234", role: "admin" };
    const hashedPassword = "hashed1234";
    const createdUser = { ...userDto, id: 1, password: hashedPassword };

    mockUserRepository.create.mockReturnValue(createdUser);
    mockUserRepository.save.mockResolvedValue(createdUser);

    const result = await service.createUser(userDto);

    expect(mockUserRepository.create).toHaveBeenCalledWith({
      ...userDto,
      password: expect.any(String),
    });
    expect(mockUserRepository.save).toHaveBeenCalledWith(createdUser);
    expect(result).toEqual(createdUser);
  });
});
