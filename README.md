# UIUcoin: Meu Primeiro Token e Ecossistema



Este repositório documenta a criação do **UIUcoin**, meu primeiro token digital. Desenvolvido com o objetivo de ser mais do que uma simples criptomoeda, o UIUcoin funciona como um **token de gratidão e retribuição**, permitindo-me recompensar aqueles que me auxiliam em diversas tarefas e favores. No futuro, os detentores de UIUcoins terão um **valor diferenciado e preferencial** ao buscarem minha ajuda, incentivando a colaboração mútua.

Todo o desenvolvimento e as ferramentas de gerenciamento do UIUcoin são baseados na **Foundry**, um conjunto de ferramentas rápido, portátil e modular para o desenvolvimento de aplicações Ethereum/EVM.

------



## 1. Tecnologias Utilizadas

O projeto UIUcoin é construído e gerenciado principalmente com o ecossistema Foundry, que inclui:

- **Forge**: Um framework de testes para Ethereum.
- **Cast**: Uma ferramenta de linha de comando para interagir com smart contracts EVM, enviar transações e obter dados da blockchain.
- **Anvil**: Um nó Ethereum local para desenvolvimento e testes rápidos.
- **Chisel**: Um REPL (Read-Eval-Print Loop) para Solidity.

------



## 2. O Contrato UIUCOIN

O coração do UIUcoin é seu contrato inteligente, implementado na blockchain e seguindo os padrões de tokens ERC-20, além de incorporar funcionalidades de controle de acesso.

Solidity

```
// SPDX-License-Identifier: MIT
// Compatible with OpenZeppelin Contracts ^5.0.0
pragma solidity ^0.8.27;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable/Ownable.sol"; // Corrigido o caminho para OpenZeppelin 5.0.0+

contract UIUCOIN is ERC20, Ownable {
    constructor(address initialOwner)
        ERC20("UIUCOIN", "UIU")
        Ownable(initialOwner)
    {}

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```



### 2.1. Padrões Utilizados

- **ERC-20**: Define as funcionalidades básicas do token, como nome (`UIUCOIN`), símbolo (`UIU`), total supply, balanços, e métodos para transferir e aprovar transferências.
- **Ownable**: Fornece um mecanismo de controle de acesso, onde um único endereço (o **proprietário**) tem privilégios exclusivos para executar certas funções administrativas.



### 2.2. Funções do Contrato

- **`constructor(address initialOwner)`**:
  - Executado apenas uma vez, na implantação do contrato.
  - Inicializa o token ERC-20 com nome "UIUCOIN" e símbolo "UIU".
  - Define o `initialOwner` como o proprietário do contrato, concedendo-lhe privilégios administrativos.
- **`function mint(address to, uint256 amount) public onlyOwner`**:
  - Permite a **cunhagem (criação) de novos tokens UIUCOIN**.
  - O modificador `onlyOwner` garante que **apenas o proprietário do contrato** pode chamar esta função, mantendo o controle sobre a oferta do token.
  - Cria e distribui a `amount` especificada de tokens para o endereço `to`.

------



## 3. Script de Deploy do UIUCOIN

A implantação do contrato `UIUCOIN` é realizada através de um script Solidity, que permite um processo de deploy automatizado e repetível.

### 3.1. Estrutura Típica do Script `UIUCOIN.s.sol`

Um script de deploy Foundry para o `UIUCOIN` geralmente segue este padrão:

Solidity

```
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import {Script, console2} from "forge-std/Script.sol";
import {UIUCOIN} from "../src/UIUCOIN.sol"; // Ajuste o caminho se necessário

contract UIUCOINDeployScript is Script {
    function run() public returns (UIUCOIN uiucoin) {
        // Obter a chave privada do deployer de forma segura (e.g., de variáveis de ambiente)
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        // Iniciar a transmissão da transação. As transações serão assinadas com a chave privada.
        vm.startBroadcast(deployerPrivateKey);

        // Implantação do contrato UIUCOIN, passando o endereço do deployer como initialOwner.
        uiucoin = new UIUCOIN(msg.sender);

        console2.log("UIUCOIN implantado em:", address(uiucoin));

        // Finalizar a transmissão.
        vm.stopBroadcast();
    }
}
```



### 3.2. Como Executar o Script



Para implantar o contrato UIUCOIN em uma rede blockchain (como Sepolia, Goerli ou mesmo um Anvil local), use o comando `forge script`:

Bash

```
forge script script/UIUCOIN.s.sol:UIUCOINDeployScript \
    --rpc-url <SUA_URL_RPC_DA_REDE> \
    --broadcast \
    --verify \
    -vvvv \
    --private-key <SUA_CHAVE_PRIVADA>
```

**Importante**: Para segurança, **nunca exponha sua chave privada diretamente no comando ou no código-fonte!** Use variáveis de ambiente (e.g., export `PRIVATE_KEY=0x...`) ou ferramentas de gerenciamento de segredos.

------



## 4. Comandos Foundry

Para começar a trabalhar com o projeto UIUcoin, clone o repositório e utilize os seguintes comandos do Foundry:

- **Construir o Projeto:**

  Bash

  ```
  forge build
  ```

- **Executar Testes:**

  Bash

  ```
  forge test
  ```

- **Formatar o Código:**

  Bash

  ```
  forge fmt
  ```

- **Gerar Gas Snapshots:**

  Bash

  ```
  forge snapshot
  ```

  ```
  
  ```

- **Obter Ajuda:**

  Bash

  ```
  forge --help
  ```

------



## 5. Exemplo de Configuração: `foundry.toml`



O arquivo `foundry.toml` é o arquivo de configuração principal para projetos Foundry, permitindo que você personalize o comportamento da compilação, testes e scripts.

Ini, TOML

```
[profile.default]
src = "src"       # Caminho para seus arquivos de contrato Solidity
out = "out"       # Caminho para onde os artefatos de build serão salvos
libs = ["lib"]    # Caminho para suas bibliotecas de dependência (ex: OpenZeppelin)
test = "test"     # Caminho para seus arquivos de teste
script = "script" # Caminho para seus scripts de deploy

# Otimização do compilador Solidity (solc)
optimizer = true
optimizer_runs = 200 # Número de execuções do otimizador

# Configurações de RPC (opcional, mas comum para ambientes de deploy)
# [rpc_endpoints]
# sepolia = "https://sepolia.infura.io/v3/SUA_CHAVE_INFURA"

# Configurações para o Etherscan (para verificação de contratos)
# [etherscan]
# sepolia = { key = "SUA_CHAVE_API_ETHERSCAN" }

# Nível de verbosidade padrão para logs (0-5)
verbosity = 3
```

