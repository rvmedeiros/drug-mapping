import {
  IsString,
  IsNotEmpty,
  MinLength,
  IsOptional,
  IsBoolean,
} from "class-validator";

export class CreateUserDto {
  @IsString()
  @IsNotEmpty()
  username!: string;

  @IsString()
  @IsNotEmpty()
  @MinLength(6)
  password!: string;

  @IsString()
  @IsNotEmpty()
  role!: string;

  @IsBoolean()
  @IsOptional()
  isActive?: boolean;
}
