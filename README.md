# DeFi Playground

A playground to interact with DeFi protocols deployed on Ethereum.

<p align="center">
	<img width=300 src="./media/building-blocks-small.png">
</p>

## About

This repository is intended to kick-start new DeFi protocol deployments. It should help to setup a local development environment with all Ethereum contracts deployed without the need to go through each project's deploy scripts. Here are the cool features of this project:

- No need to deploy smart contracts yourself, just start the local blockchain and have all your favourite DeFi protocols available.
- A standard interface to get the contract's ABIs to use in your own projects.
- Quickly deploy new apps and smart contracts.

The project makes use of ganache-cli's feature to fork an existing blockchain into your own test environment.

### Built with

- [Python 3](https://www.python.org/)
- [ganache-cli](https://github.com/trufflesuite/ganache-cli)

## Getting started

### Prerequisites

You need to have a current version of the Ethereum main chain operating. By default, `defi-playground` will check for an Ethereum node running on `localhost:8545`. This could be your [Geth](https://github.com/ethereum/go-ethereum) or [Open Ethereum](https://github.com/openethereum/openethereum) node.

Alternatively, you can also use [Infura](https://infura.io/) and their hosted nodes. To get started, follow their tutorials to [create an account and a project id](https://infura.io/docs). Once you have a project id, create an environment variable in your shell environment. For example, put this in your `~/.bash_profile`, `~/.profile`, or `~/.zshrc`:

```bash
export INFURA_PLAY_ID="your-project-id-goes-here"
```

### Installation

Clone the repository.

```bash
git clone git@github.com:nud3l/defi-playground.git
```

Install dependencies.

```bash
make init
```

## Usage

From the root folder of the repository, run defi-playground.

```bash
make defi-playground
```

Or directly via python:
```bash
python -m playground
```

This will start your ganache-cli node. You can configure parameters submitted to Ganache yourself that are included in `play.config`.

From then you can just import accounts from a file `accounts.json` created in the root folder of this repository. Alternatively, you can use the fixed mnemonic in your apps as well.

## High-Level Integration Examples

Below are an example of how to use defi-playground together with Maker and Uniswap. In both cases, their SDKs and libraries are used that are aware of the deployed contract addresses and [ABIs](https://solidity.readthedocs.io/en/develop/abi-spec.html). 

### Maker `dai.js`

You could create a Vault in Maker using `dai.js` from the [example in the Maker docs](https://docs.makerdao.com/dai.js/getting-started#create-a-vault):

```js
import { McdPlugin, ETH, MDAI } from '@makerdao/dai-plugin-mcd';

// you provide these values from accounts.json
const myPrivateKey = 'your-private-key';

const maker = await Maker.create('http', {
  plugins: [McdPlugin],
  url: `https://localhost:2000`,
  privateKey: myPrivateKey
});

// verify that the private key was read correctly
console.log(maker.currentAddress());

// make sure the current account owns a proxy contract;
// create it if needed. the proxy contract is used to 
// perform multiple operations in a single transaction
await maker.service('proxy').ensureProxy();

// use the "vault manager" service to work with vaults
const manager = maker.service('mcd:cdpManager');
  
// ETH-A is the name of the collateral type; in the future,
// there could be multiple collateral types for a token with
// different risk parameters
const vault = await manager.openLockAndDraw(
  'ETH-A', 
  ETH(50), 
  MDAI(1000)
);

console.log(vault.id);
console.log(vault.debtValue); // '1000.00 DAI'
```

### Uniswap Frontend Integration 

*FIXME*: update this to a full working example

You could trade tokens on Uniswap using their [integration](https://uniswap.org/docs/v1/frontend-integration/connect-to-uniswap/):

```js
// buy ETH
const outputAmount = 100
const inputReserve = web3.eth.getBalance(exchangeAddress)
const outputReserve = tokenContract.methods.balanceOf(exchangeAddress).call()
```



## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are greatly appreciated.

1. Fork the Project
2. Create your Feature Branch (git checkout -b feature/AmazingFeature)
3. Commit your Changes (git commit -m 'Add some AmazingFeature')
4. Push to the Branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Dominik Harz  - [@dominik0](https://twitter.com/dominik0_)
