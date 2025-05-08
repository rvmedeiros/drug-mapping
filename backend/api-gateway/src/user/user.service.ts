import { Injectable, OnModuleInit, Logger } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Repository } from "typeorm";
import * as bcrypt from "bcrypt";

import { User } from "./user.entity";
import { CreateUserDto } from "./create-user.dto";

@Injectable()
export class UserService implements OnModuleInit {
  private readonly logger = new Logger(UserService.name);

  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>
  ) {}

  private async ensureAdminUser() {
    const adminUsername = "admin";
    const adminPassword = "admin123";
    const adminRole = "admin";

    const existingAdmin = await this.userRepository.findOne({
      where: { username: adminUsername },
    });

    if (!existingAdmin) {
      const hashedPassword = await bcrypt.hash(adminPassword, 10);
      const adminUser = this.userRepository.create({
        username: adminUsername,
        password: hashedPassword,
        role: adminRole,
        isActive: true,
      });

      await this.userRepository.save(adminUser);
      this.logger.log("Admin user created successfully");
    } else {
      this.logger.log("Admin user already exists");
    }
  }

  async onModuleInit() {
    await this.ensureAdminUser();
  }

  async createUser(userDto: CreateUserDto): Promise<User> {
    const hashedPassword = await bcrypt.hash(userDto.password, 10);
    const user = this.userRepository.create({
      username: userDto.username,
      password: hashedPassword,
      role: userDto.role,
    });
    return this.userRepository.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.userRepository.find();
  }

  async findById(id: number): Promise<User | null> {
    return this.userRepository.findOne({ where: { id } });
  }

  async findByUsername(username: string): Promise<User | null> {
    return this.userRepository.findOne({ where: { username } });
  }

  async updateUser(id: number, updateDto: Partial<User>): Promise<User | null> {
    if (updateDto.password) {
      updateDto.password = await bcrypt.hash(updateDto.password, 10);
    }
    await this.userRepository.update(id, updateDto);
    return this.findById(id);
  }

  async deleteUser(id: number): Promise<void> {
    await this.userRepository.delete(id);
  }
}
