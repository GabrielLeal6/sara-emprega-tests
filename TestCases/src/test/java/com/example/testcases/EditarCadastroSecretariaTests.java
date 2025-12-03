package com.example.testcases;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.*;

import java.time.Duration;

import static org.junit.Assert.*;

public class EditarCadastroSecretariaTests {

    private WebDriver driver;
    private WebDriverWait wait;

    // ===== PAGE OBJECT =====
    private By inputNome = By.name("nome");
    private By inputEmail = By.name("email");
    private By inputTelefone = By.name("telefone");
    private By inputEndereco = By.name("endereco");

    private By btnEditar = By.xpath("//button[contains(., 'Alterar Dados')]");
    private By btnSalvar = By.xpath("//button[contains(., 'Confirmar')]");

    private By toast = By.cssSelector("div[role='alert']");
    private By mensagemErro = By.cssSelector("p.text-red-500");

    @Before
    public void setup() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.manage().window().maximize();

        driver.get("https://sara-frontend-736daffd516a.herokuapp.com/perfil/secretaria");
    }

    @After
    public void tearDown() {
        if (driver != null) driver.quit();
    }

    // ===== UTIL =====

    private void clicar(By elemento) {
        wait.until(ExpectedConditions.elementToBeClickable(elemento)).click();
    }

    private void preencher(By campo, String valor) {
        WebElement el = wait.until(ExpectedConditions.visibilityOfElementLocated(campo));
        el.clear();
        el.sendKeys(valor);
    }

    private String texto(By seletor) {
        try {
            return wait.until(ExpectedConditions.visibilityOfElementLocated(seletor)).getText();
        } catch (Exception e) {
            return "";
        }
    }

    private void habilitarEdicao() {
        clicar(btnEditar);
    }

    // =====================================================================================
    // CT-006.01 - Alteração completa com sucesso
    // =====================================================================================

    @Test
    public void editarComSucesso() {
        habilitarEdicao();

        preencher(inputNome, "Ana Silva Santos");
        preencher(inputEmail, "ana.santos+" + System.currentTimeMillis() + "@semas.gov.br");
        preencher(inputTelefone, "(81) 91234-5678");
        preencher(inputEndereco, "Travessa A, 100");

        clicar(btnSalvar);

        assertTrue(texto(toast).contains("Cadastro atualizado com sucesso"));
    }

    // =====================================================================================
    // CT-006.02 - Alteração parcial (apenas um campo)
    // =====================================================================================

    @Test
    public void edicaoParcial() {
        habilitarEdicao();

        preencher(inputTelefone, "(81) 99876-4321");

        clicar(btnSalvar);

        assertTrue(texto(toast).contains("Cadastro atualizado com sucesso"));
    }

    // =====================================================================================
    // CT-006.03 - Campo obrigatório vazio impede atualização
    // =====================================================================================

    @Test
    public void impedeSalvarComCampoObrigatorioVazio() {
        habilitarEdicao();

        preencher(inputNome, "");

        clicar(btnSalvar);

        assertTrue(texto(mensagemErro).contains("Preencha todos os campos obrigatórios"));
    }

    // =====================================================================================
    // CT-006.04 - Erro ao salvar com e-mail já cadastrado
    // =====================================================================================

    @Test
    public void emailJaCadastrado() {
        habilitarEdicao();

        preencher(inputEmail, "secretaria@daqui.com");

        clicar(btnSalvar);

        assertTrue(texto(toast).contains("Este e-mail já está cadastrado"));
    }

    // =====================================================================================
    // CT-006.05 - Falha técnica impede atualização
    // =====================================================================================

    @Test
    public void falhaAoAtualizar() {
        habilitarEdicao();

        // Valor que simula falha
        preencher(inputEndereco, "###@@invalid");

        clicar(btnSalvar);

        assertTrue(texto(toast).contains("Não foi possível atualizar o cadastro"));
    }

}
