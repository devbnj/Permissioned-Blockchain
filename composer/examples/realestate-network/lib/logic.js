'use strict';

/**
* A transaction processor function description
* This comment is of utmost importance - meta-data
* @param {com.devb.realestate.Escrow} parameter-name 
* @transaction
*/

function escrow(tx) {
    var homeValue = tx.escrowBook.home.value;
    var buyer = tx.buyer;
    var money = tx.money;
    var document = tx.document;
  }
  
  /**
  * A transaction processor function description
  * @param {com.devb.realestate.ListProperty} parameter-name 
  * @transaction
  */
  function listProperty(tx) {
    this.home = tx.home;
    var assetRegistry;  
    var id = tx.home.propertyId;
    return getAssetRegistry('com.devb.mortgage.PropertyHome')
        .then(function(ar) {
            assetRegistry = ar;
            return assetRegistry.get(id);
        })
        .then(function(asset) {
            // asset = tx.home;
            asset.propertyStatus = ts.propStatus;
            return assetRegistry.update(asset);
        });
  }
  
  /**
  * A transaction processor function description
  * @param {com.devb.realestate.Revalue} parameter-name 
  * @transaction
  */
  function revalue(tx) {
    var assetRegistry;  
    var id = tx.relatedAsset.propertyId;
    // Save the old value of the property.
    var oldValue = tx.home.value;
    // Update the property with the new value.
    tx.home.value = tx.newValue;
    return getAssetRegistry('com.devb.mortgage.PropertyHome')
        .then(function(ar) {
            assetRegistry = ar;
            return assetRegistry.get(id);
        })
        .then(function(asset) {
            asset.value = tx.newValue;
            return assetRegistry.update(asset);
        });
  }  
  
