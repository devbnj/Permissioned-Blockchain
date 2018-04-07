'use strict';

/**
 * Revalue transaction
 * @param {com.devb.consolidated.Revalue} tx
 * @transaction
 */
async function revalue(tx) {
    const oldValue = tx.asset.value;
    tx.asset.value = tx.newValue;
    const assetRegistry = await getAssetRegistry('com.devb.consolidated.Portfolio');
    await assetRegistry.update(tx.asset);
}
