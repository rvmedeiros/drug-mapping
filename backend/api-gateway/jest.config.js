module.exports = {
  roots: ["<rootDir>/src"],
  testRegex: ".*.spec.ts$",
  transform: {
    "^.+\\.(t|j)s$": "ts-jest",
  },
  moduleFileExtensions: ["js", "json", "ts"],
  testEnvironment: "node",
};
