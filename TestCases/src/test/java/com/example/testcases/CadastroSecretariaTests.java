package com.example.testcases;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

import static org.junit.Assert.assertTrue;

public class CadastroSecretariaTests {

    private WebDriver driver;
    private WebDriverWait wait;

    // ===== PAGE OBJECT =====
    private By inputNome = By.id("nome");
    private By inputEndereco = By.id("endereco");
    private By inputEmail = By.id("email");
    private By inputSenha = By.id("senha");
    private By btnSolicitar = By.cssSelector("button[type='submit']");
    private By mensagemErro = By.cssSelector("p.text-red-500");
    private By toast = By.cssSelector("div[role='alert']");

    @Before
    public void setup() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
        driver.manage().window().maximize();
        driver.get("https://sara-frontend-736daffd516a.herokuapp.com/cadastro/secretaria");
    }

    @After
    public void teardown() {
        if (driver != null) driver.quit();
    }

    // ===== UTILITÁRIOS =====
    private void preencher(By campo, String valor) {
        WebElement el = wait.until(ExpectedConditions.visibilityOfElementLocated(campo));
        el.clear();
        el.sendKeys(valor);
    }

    private void clicar(By elemento) {
        wait.until(ExpectedConditions.elementToBeClickable(elemento)).click();
    }

    private String getTextoSeExistir(By seletor) {
        try {
            WebElement el = wait.until(ExpectedConditions.visibilityOfElementLocated(seletor));
            return el.getText();
        } catch (Exception e) {
            return "";
        }
    }

    // ===== TESTES =====

    @Test
    public void cadastroComSucesso() {
        preencher(inputNome, "Ana");
        preencher(inputEndereco, "Rua A, 100");
        preencher(inputEmail, "ana.silva+" + System.currentTimeMillis() + "@teste.com");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("Aguarde a aprovação"));
    }

    @Test
    public void impedeCadastroComCampoVazio() {
        preencher(inputNome, "");
        preencher(inputEndereco, "Rua A");
        preencher(inputEmail, "teste@teste.com");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(mensagemErro).contains("pelo menos 3 caracteres"));
    }

    @Test
    public void emailJaExiste() {
        preencher(inputNome, "Maria");
        preencher(inputEndereco, "Rua B");
        preencher(inputEmail, "contato@secretaria.gov");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("E-mail já está cadastrado"));
    }

    @Test
    public void cadastroViaLinkDireto() {
        preencher(inputNome, "Julia");
        preencher(inputEndereco, "Avenida 10");
        preencher(inputEmail, "julia+" + System.currentTimeMillis() + "@teste.com");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("Aguarde a aprovação"));
    }

    @Test
    public void emailInvalido() {
        preencher(inputNome, "Fernanda");
        preencher(inputEndereco, "Rua C");
        preencher(inputEmail, "fernanda@");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("E-mail inválido"));
    }

    @Test
    public void loginAposAprovacao() {
        preencher(inputEmail, "usuario_aprovado@test.com");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("Área restrita"));
    }

    @Test
    public void loginNegadoSemAprovacao() {
        preencher(inputEmail, "usuario_pendente@test.com");
        preencher(inputSenha, "Senha@123");

        clicar(btnSolicitar);

        assertTrue(getTextoSeExistir(toast).contains("E-mail ou senha inválidos"));
    }
}
