cmake_minimum_required(VERSION 3.8)
project(lol)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()

# Instala el launch para que 'ros2 launch lol leoni.launch.py' lo encuentre
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)
