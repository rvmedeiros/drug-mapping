import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { UserModule } from './user/user.module';
import { typeOrmConfig, typeOrmFeature } from './config/ormconfig';

@Module({
  imports: [TypeOrmModule.forRoot(typeOrmConfig), typeOrmFeature, UserModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
