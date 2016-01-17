var deckBuilder = angular.module('deck-builder', ['ngMaterial', 'ngTable'])
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

    $scope.addToDeck = function() {
      $scope.deck.push($scope.selectedItem.value);
    }

    $scope.deck = [];
  }]);
