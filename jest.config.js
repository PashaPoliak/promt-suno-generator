module.exports = {
  transformIgnorePatterns: [
    "node_modules/(?!(axios|@?react-router|@?react-router-dom|@?@?react-hook-form)/)"
  ],
  testEnvironment: "jsdom",
  setupFilesAfterEnv: ["<rootDir>/src/setupTests.ts"],
  moduleNameMapper: {
    "\\.(css|less|scss|sass)$": "identity-obj-proxy"
 }
};