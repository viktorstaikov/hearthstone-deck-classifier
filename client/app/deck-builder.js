var deckBuilder = angular.module('deck-builder', ['ngMaterial', 'smart-table'])
  .controller('DeckController', ['$scope', '$http', function($scope, $http) {
    $scope.getMatches = function() {
      var url = 'https://omgvamp-hearthstone-v1.p.mashape.com/cards/search/'
        + $scope.searchText;

      return $http({
        method: 'GET',
        url: url,
        headers: {
          'X-Mashape-Key': 'MQ5WRXL3ZEmshqn6OmLnz32G5ayop1KTodkjsnOUbuooXww9Uu'
        }})
        .then(function success(response) {
          displayData = [];
          for (i in response.data) {
            displayData.push({
              display: response.data[i].name,
              value: response.data[i].name
            });
          }
          return displayData;
        });
    };

    var getCardIndex = function(cardName) {
      for (i in $scope.deck) {
        if ($scope.deck[i]['card-name'] === cardName) {
          return i;
        }
      }

      return -1;
    };

    var updateClassifier = function() {

    };

    $scope.addToDeck = function() {
      if (!$scope.selectedItem) {
        return;
      }

      var card =  $scope.selectedItem.value
      var cardIndex = getCardIndex(card);
      if (cardIndex !== -1) {
        $scope.deck[cardIndex]['card-count'] += 1;
        return;
      }

      $scope.deck.push({
        'card-name': $scope.selectedItem.value,
        'card-count': 1
      });

      $scope.searchText = '';
      updateClassifier();
    };

    $scope.removeFromDeck = function(card) {
      cardIndex = getCardIndex(card['card-name']);
      if (cardIndex === -1) {
        return;
      }

      $scope.deck[cardIndex]['card-count']--;
      if ($scope.deck[cardIndex]['card-count'] <= 0) {
        $scope.deck.splice(cardIndex, 1);
      }
    };

    $scope.displayedRows = [];
    $scope.deck = [];
  }]);
