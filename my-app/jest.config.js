module.exports = {
  testEnvironment: "jsdom",
  moduleNameMapper: {
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
  },
  setupFilesAfterEnv: ["@testing-library/jest-dom", "./jest.setup.js"],
};