# Устанавливаем переменные
PYTHON := python3
PIP := pip3
VENV_DIR := venv
STEPS := 2 3 4 5 6
TEST_DIR := course/steps

# Устанавливаем виртуальное окружение и зависимости
.PHONY: setup
setup:
	$(PYTHON) -m venv $(VENV_DIR)  # Создание виртуального окружения
	. $(VENV_DIR)/bin/activate && $(PIP) install -r requirements.txt  # Установка зависимостей

# Запуск всех тестов
.PHONY: test
test: test_step_2 test_step_3 test_step_4 test_step_5 test_step_6

# Запуск тестов для конкретного шага
.PHONY: test_step
test_step:
	@echo "Запуск тестов для шага $(step)"
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-$(step)/test_step_$(step).py

# Тесты для каждого шага
test_step_2:
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-2/test_step_2.py

test_step_3:
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-3/test_step_3.py

test_step_4:
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-4/test_step_4.py

test_step_5:
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-5/test_step_5.py

test_step_6:
	. $(VENV_DIR)/bin/activate && pytest $(TEST_DIR)/step-6/test_step_6.py

# Очистка окружения
.PHONY: clean
clean:
	rm -rf $(VENV_DIR)
