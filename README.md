# Testes E2E (Fim a Fim) - SARA EMPREGA

Este repositório contém os testes de automação para a validação da qualidade do produto deployado.

### STACK

* **Linguagem:** Python 3.x
* **Automação:** Selenium WebDriver
* **Framework:** Pytest

---

### Como configurar e rodar

1.  **Crie o Ambiente Virtual (Isolamento):**
    ```bash
    python3 -m venv venv_e2e
    ```

2.  **Ative o Ambiente:**
    ```bash
    # Unix: source venv_e2e/bin/activate 
    # Windows: .\venv_e2e\Scripts\activate
    ```

3.  **Instale as Dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Executar todos os testes:**
    * (se o deploy estiver no ar) *
    ```bash
    pytest tests_e2e/specs/
    ```
    *(Para rodar um teste específico, use `pytest tests_e2e/specs/test_login.py`)*