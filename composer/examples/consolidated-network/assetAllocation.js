/* eslint-disable */
/* jshint esversion:6 */
let pa = require('portfolio-allocation');

let AssetAllocation = class {
    constructor(portfolioSize, portfolioType) {
        this.portfolioSize = portfolioSize;
        this.portfolioType = portfolioType;
    }

    // Assets allocation module 
    doWeightedRisk() {
        // Rounded weights portfolio
        console.log('Rounded Weights');
        // Example with static data
        let testValues = [
            [0.7373, 0.2627, 0],
            [0.5759, 0.0671, 0.3570],
            [0.22, 0.66, 0.12],
            [0.22, 0.66, 0.12],
            [0.5, 0.49, 0.01]
        ];
        let testGridIndices = [10, 10, 1, 5, 1];

        let reslt;
        let i = 0;
        console.log('Examples of rounding.')
        console.log('Use the rounded weights with AA')
        for (i = 0; i < testValues.length; ++i) {
            reslt = pa.roundedWeights(testValues[i], testGridIndices[i]);
            console.log(reslt);
        }
        
        // Covariance matrix
        let sigma = [
            [0.0100, 0.0090, 0.0010],
            [0.0090, 0.0100, 0.0010],
            [0.0010, 0.0010, 0.0100]
        ];

        // Compute MDP weights
        let wts = pa.mostDiversifiedWeights(sigma, {eps: 1e-10, maxIter: 10000});
        console.log('Example of most diversified weights.')
        console.log(wts);

        console.log('Example Equal Weights');
        // Generate a number of assets 
        let pList = Math.floor(Math.random() * (this.portfolioSize - 1 + 1) + 1);
        // Compute Equal Weights
        wts = pa.equalWeights(pList);
        console.log('Equal weights for portfolio size '+pList)
        console.log(wts);

        console.log('Example Equal Risk');
        // use the same list
        // Generate n random variances
        let sigma1 = new Array(pList);
        for (let i = 0; i < pList; ++i) {
            sigma1[i] = 1 - Math.random();
        }
        // Compute ERB weights
        wts = pa.equalRiskBudgetWeights(sigma1);
        // Check the number of output weights
        console.log('Portfolio size '+wts.length);
        console.log(wts);

        // ERC portfolio
        wts = pa.equalRiskContributionWeights([[0.1, 0, 0], [0, 0.2, 0], [0, 0, 0.3]]); 
        console.log('Equal risk contribution ');
        console.log(wts);

        /*
        // MCA portfolio
        wts = pa.minCorrWeights([[0.1, 0], [0, 0.2]]);
        console.log('Minimum correlation weights');
        console.log(wts);

        wts = pa.clusterRiskParityWeights([[0.1,0], [0,0.2]], {clusteringMode: 'ftca'});
        console.log(wts)
        */        
    }
}

// program starts here
console.log('** Program start **');
let aa = new AssetAllocation(18, "equalWeights");
aa.doWeightedRisk();
console.log('** Program end **');
// program ends here