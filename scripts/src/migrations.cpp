#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <filesystem>
#include <algorithm>
#include <iterator>
#include <cstdlib>
#include <dotenv.h>
#include <SQLiteCpp/SQLiteCpp.h>

/**
 * @brief Get the migrations alredy executed.
 * 
 * @param db Database
 * @return std::vector<std::string> Migration's names
 */
std::vector<std::string> getCurrentMigrations(SQLite::Database &db) {
  std::vector<std::string> results;
  try {
    SQLite::Statement query(db, "SELECT name FROM migration ORDER BY name");
    while (query.executeStep()) {
      results.push_back(query.getColumn("name").getText());
    }
  } catch (std::exception &e) {
    std::cerr << "Warning: " << e.what() << std::endl;
  }
  return results;
}

/**
 * @brief Verifies the end of a string.
 * 
 * @param str String
 * @param suffix End
 * @return true If str ends with suffix
 * @return false If str doesn't end with suffix
 */
bool ends_with(const std::string& str, const std::string& suffix) {
  if (str.length() >= suffix.length()) {
    return (0 == str.compare(str.length() - suffix.length(), suffix.length(), suffix));
  } else {
    return false;
  }
}

/**
 * @brief Get the Files in the migration's path.
 * 
 * Read all the file's names and return an vector with
 * the names of the files that ends with .sql.
 *
 * @param path Path of the migrations
 * @return std::vector<std::string> 
 */
std::vector<std::string> getFiles(const std::string &path) {
  namespace fs = std::filesystem;
  std::vector<std::string> files;
  for (const auto & entry : fs::directory_iterator(path)) {
    std::string fileName = entry.path().filename().string();
    if (ends_with(fileName, ".sql"))
      files.push_back(fileName);
  }
  sort(files.begin(), files.end());
  return files;
}

/**
 * @brief Get the migrations not executed yet.
 * 
 * Deletes from the getFile's vector all the files from getCurrenMigration.
 *
 * @param path Path of the migrations
 * @param db Database
 * @return std::vector<std::string> 
 */
std::vector<std::string> getDiference(const std::string &path, SQLite::Database &db) {
  std::vector<std::string> result;
  std::vector<std::string> files = getFiles(path);
  std::vector<std::string> applied = getCurrentMigrations(db);
  std::set_difference(
    files.begin(), files.end(),
    applied.begin(), applied.end(),
    std::back_inserter(result)
  );
  return result;
}

/**
 * @brief Read's the content of a file.
 * 
 * @param path Path to the file.
 * @return std::string 
 */
std::string getFileContent(const std::string &path) {
  std::ifstream file(path);
  std::string str;
  std::string fileContent;

  while (getline(file, str)) {
    fileContent += str;
    fileContent.push_back('\n');
  }

  return fileContent;
}

/**
 * @brief Run the code of a migration.
 *
 * Uses an transaction, is there are an error, makes an rollback.
 * 
 * @param db Database
 * @param migration Migration's content
 * @return true 
 * @return false 
 */
bool runMigration(SQLite::Database &db, const std::string &migration) {
  try {
    std::string fullQuery = getFileContent(migration);
    std::stringstream ss(fullQuery);
    std::string segment;

    SQLite::Transaction transaction(db);

    while (getline(ss, segment, ';')) {
      segment.erase(0, segment.find_first_not_of(" \n\r\t"));
      segment.erase(segment.find_last_not_of(" \n\r\t") + 1);

      if (!segment.empty()) {
        db.exec(segment);
      }
    }

    std::string migrationName = migration.substr(migration.find_last_of('/') + 1);
    db.exec("INSERT INTO migration (name) VALUES ('" + migrationName + "')");

    transaction.commit();
    std::cout << "Migration " << migrationName << " completed and stored." << std::endl;

    return true;
  } catch (std::exception &e) {
    std::cerr << "Error at migration: " << e.what() << std::endl;
    std::cerr << "ROLLBACK..." << std::endl;
    return false;
  }
}

/**
 * @brief Conects to the database and runs the migrations.
 * 
 * @return int
 */
int main() {
  dotenv::init("/home/santiago/Projects/web/ToDo/.env");
  std::string migrationsPath = std::getenv("MIGRATIONS");
  std::string database = std::getenv("DATABASE");

  try {
    SQLite::Database db(database, SQLite::OPEN_READWRITE | SQLite::OPEN_CREATE);

    std::vector<std::string> files = getDiference(migrationsPath, db);

    for (size_t i = 0; i < files.size(); i++) {
      bool res = runMigration(db, migrationsPath + "/" + files[i]);
      if (!res)
        return 1;
    }

  } catch (std::exception &e) {
    std::cerr << "Exception: " << e.what() << std::endl;
    return 1;
  }

  return 0;
}
