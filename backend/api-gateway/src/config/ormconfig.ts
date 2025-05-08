import { TypeOrmModuleOptions, TypeOrmModule } from '@nestjs/typeorm';
import { User } from '../user/user.entity';

export const typeOrmConfig: TypeOrmModuleOptions = {
  type: 'postgres',
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  username: process.env.DB_USERNAME || 'admin',
  password: process.env.DB_PASSWORD || '1234',
  database: process.env.DB_NAME || 'drug_indications',
  entities: [User],
  synchronize: true,
};

export const typeOrmFeature = TypeOrmModule.forFeature([User]);
