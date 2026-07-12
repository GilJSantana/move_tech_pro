# MoveTech × Magalu Cloud — Projeto Final E-Commerce Fim a Fim

Este repositório contém a arquitetura de referência e a esteira de automação CI/CD para o projeto prático final do treinamento **MoveTech**, patrocinado pela **Magalu Cloud**. O objetivo deste laboratório é consolidar as competências de administração de sistemas, redes, conteinerização, orquestração, banco de dados gerenciado e cultura DevOps em um único pipeline convergente.

---

## 🏗️ 1. Arquitetura da Solução

A aplicação simula um fluxo simplificado de e-commerce projetado para validar a comunicação e o isolamento entre camadas na infraestrutura da Magalu Cloud:

*   **Camada de Apresentação (Frontend):** Uma aplicação estática baseada em Nginx que serve a interface do usuário na porta pública `30080` via Kubernetes NodePort.
*   **Camada de Negócio (Backend API):** Uma API desenvolvida em FastAPI (Python) que processa as requisições de compra, exposta na porta pública `30081` via NodePort.
*   **Camada de Persistência (Banco de Dados):** Uma instância gerenciada de PostgreSQL provida pelo **Magalu DBaaS**, isolada logicamente em uma sub-rede privada sem IP público.
*   **Orquestração local:** Um cluster leve de nó único gerenciado pelo **K3s** rodando dentro de uma máquina virtual (Compute) Ubuntu.

---

## 🛠️ 2. Mapeamento de Cobertura do Treinamento

O projeto foi desenhado para que nenhuma competência do treinamento seja deixada de lado:

| Módulo / Competência | Implementação Prática no Projeto |
| :--- | :--- |
| **1. Fundamentos & Linux** | Escrita do script de automação de bootstrap (`install-k3s.sh`) e gerência do S.O. da VM. |
| **2. Serviços de Cloud** | Provisionamento declarativo de VPC, Sub-redes, Security Groups e instâncias de Computação. |
| **3. DevOps & Containers** | Criação de Dockerfiles otimizados multi-stage e escrita do workflow no GitHub Actions. |
| **4. Gestão de Dados** | Acoplamento seguro da API ao serviço de DBaaS PostgreSQL utilizando variáveis de ambiente. |
| **5. Observabilidade** | Coleta de logs estruturados de Pods (`kubectl logs`) e monitoramento de saúde via endpoint `/health`. |
| **6. Arquitetura** | Análise de trade-offs de rede, segurança perimetral e viabilidade financeira (K3s em VM vs K8s Gerenciado). |

---

## 🔄 3. Funcionamento da Esteira (Princípio da Idempotência)

O workflow do GitHub Actions (`.github/workflows/deploy.yml`) opera sob o conceito de **infraestrutura convergente**. Em vez de simplesmente falhar caso os recursos já existam, a esteira utiliza a CLI da Magalu Cloud (`mgc`) para inspecionar o ambiente:

```text
[Disparo do Commit]
       │
       ▼
┌──────────────────────────────┐
│  MGC CLI: Existe a VPC?      ├─(Não)─► Criar VPC e Security Groups
└──────┬───────────────────────┘
       │(Sim)
       ▼
┌──────────────────────────────┐
│  MGC CLI: Existe o DBaaS?    ├─(Não)─► Criar Instância PostgreSQL Gerenciada
└──────┬───────────────────────┘
       │(Sim)
       ▼
┌──────────────────────────────┐
│  MGC CLI: Existe a VM K3s?   ├─(Não)─► Criar VM Ubuntu + Injetar User Data (install-k3s.sh)
└──────┬───────────────────────┘
       │(Sim)
       ▼
┌──────────────────────────────┐
│ Build & Push das Imagens     ├─► Docker Build/Push para o Magalu Container Registry
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│ Deploy dos Manifestos K8s    ├─► Conexão SSH na VM -> Kubectl Apply nos arquivos da pasta /k8s
└──────────────────────────────┘



# MoveTech × Magalu Cloud — Projeto Final E-Commerce Fim a Fim

Este repositório contém a arquitetura de referência e a esteira de automação CI/CD para o projeto prático final do treinamento **MoveTech**, patrocinado pela **Magalu Cloud**. O objetivo deste laboratório é consolidar as competências de administração de sistemas, redes, conteinerização, orquestração, banco de dados gerenciado e cultura DevOps em um único pipeline convergente.

---

## 🏗️ 1. Arquitetura da Solução

A aplicação simula um fluxo simplificado de e-commerce projetado para validar a comunicação e o isolamento entre camadas na infraestrutura da Magalu Cloud:

*   **Camada de Apresentação (Frontend):** Uma aplicação estática baseada em Nginx que serve a interface do usuário na porta pública `30080` via Kubernetes NodePort.
*   **Camada de Negócio (Backend API):** Uma API desenvolvida em FastAPI (Python) que processa as requisições de compra, exposta na porta pública `30081` via NodePort.
*   **Camada de Persistência (Banco de Dados):** Uma instância gerenciada de PostgreSQL provida pelo **Magalu DBaaS**, isolada logicamente em uma sub-rede privada sem IP público.
*   **Orquestração local:** Um cluster leve de nó único gerenciado pelo **K3s** rodando dentro de uma máquina virtual (Compute) Ubuntu.

---

## 🛠️ 2. Mapeamento de Cobertura do Treinamento

O projeto foi desenhado para que nenhuma competência do treinamento seja deixada de lado:

| Módulo / Competência | Implementação Prática no Projeto |
| :--- | :--- |
| **1. Fundamentos & Linux** | Escrita do script de automação de bootstrap (`install-k3s.sh`) e gerência do S.O. da VM. |
| **2. Serviços de Cloud** | Provisionamento declarativo de VPC, Sub-redes, Security Groups e instâncias de Computação. |
| **3. DevOps & Containers** | Criação de Dockerfiles otimizados multi-stage e escrita do workflow no GitHub Actions. |
| **4. Gestão de Dados** | Acoplamento seguro da API ao serviço de DBaaS PostgreSQL utilizando variáveis de ambiente. |
| **5. Observabilidade** | Coleta de logs estruturados de Pods (`kubectl logs`) e monitoramento de saúde via endpoint `/health`. |
| **6. Arquitetura** | Análise de trade-offs de rede, segurança perimetral e viabilidade financeira (K3s em VM vs K8s Gerenciado). |

---

## 🔄 3. Funcionamento da Esteira (Princípio da Idempotência)

O workflow do GitHub Actions (`.github/workflows/deploy.yml`) opera sob o conceito de **infraestrutura convergente**. Em vez de simplesmente falhar caso os recursos já existam, a esteira utiliza a CLI da Magalu Cloud (`mgc`) para inspecionar o ambiente:

*   **Validação de Redes:** A esteira checa a existência da VPC e Security Groups via CLI. Se ausentes, cria a topologia e libera portas essenciais.
*   **Validação de Banco de Dados:** Checa a existência da instância do DBaaS. Se ausente, cria o banco PostgreSQL gerenciado.
*   **Validação de Computação:** Checa a existência da máquina virtual do nó K3s. Se ausente, provisiona a VM Ubuntu e injeta o script de bootstrap.
*   **Atualização de Estado:** Após validar e garantir a infraestrutura de base, a esteira executa o build das imagens Docker, publica no registry e aplica os novos manifestos do Kubernetes via acesso SSH na VM.

---

## 🔑 4. Pré-requisitos e Configuração de Secrets

Para que a esteira interaja com a sua conta da Magalu Cloud, você deve configurar os seguintes **Secrets** no seu repositório do GitHub (*Settings > Secrets and variables > Actions > New repository secret*):

1.  `MGC_API_KEY`: Sua chave de API ativa gerada no painel de gerenciamento de chaves da Magalu Cloud.
2.  `MGC_SSH_KEY`: A chave privada correspondente à chave pública associada à criação da VM (utilizada pela action de SSH para aplicar os manifestos do Kubernetes).
3.  `MGC_K3S_VM_IP`: O IP público que foi associado à sua máquina virtual após o primeiro provisionamento.

---

## 🚀 5. Como Executar e Validar o Ambiente

### Passo 1: Clonar o Repositório e Ajustar Variáveis
Clone o repositório para sua máquina local e verifique os arquivos de manifesto em `/k8s`. Certifique-se de preencher as tags de imagem apontando para o seu Registry mapeado na Magalu Cloud.

### Passo 2: O Primeiro Push (Provisionamento)
Envie as alterações para a branch principal para disparar o pipeline:
`git add .`
`git commit -m "feat: estruturando esteira idempotente de e-commerce"`
`git push origin main`
*Nota: A primeira execução demorará mais tempo, pois engloba o tempo de provisionamento do DBaaS (PostgreSQL) e o bootstrap do K3s na máquina virtual.*

### Passo 3: Validando a Aplicação
Após a conclusão do pipeline com sucesso:
1. Obtenha o IP público da instância de computação criada no painel da Magalu Cloud.
2. Acesse a interface do e-commerce através do navegador: `http://<IP_PUBLICO_DA_VM>:30080`.
3. Abra o console do desenvolvedor do navegador (F12) na aba **Rede (Network)**.
4. Clique no botão **"Simular Compra"**. 
5. Certifique-se de que a requisição retornou o código HTTP `200` vindo da API (`:30081`) contendo o ID incremental do banco de dados, confirmando a persistência ponta a ponta.

---

## 🛑 6. Comandos Úteis para Resolução de Problemas (Troubleshooting)

Caso o comportamento esperado não ocorra, acesse a VM via SSH e utilize os comandos absorvidos nos Módulos 1 e 5:

*   **Verificar logs da API (Backend):**
    `export KUBECONFIG=/etc/rancher/k3s/k3s.yaml`
    `kubectl logs -l app=backend --tail=50`
*   **Verificar o status dos Pods no cluster:**
    `kubectl get pods -A`
*   **Validar se o script de User Data terminou a instalação com sucesso:**
    `tail -f /var/log/cloud-init-output.log`
