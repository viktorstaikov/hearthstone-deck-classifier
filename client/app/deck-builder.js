var deckBuilder = angular.module('deck-builder', ['ngMaterial', 'smart-table'])
  .controller('DeckController', ['$scope', '$http', function($scope, $http) {

    var hearthstoneApiBaseUrl = 'https://omgvamp-hearthstone-v1.p.mashape.com';
    var hearthstoneApiHeaders = {
      'X-Mashape-Key': 'MQ5WRXL3ZEmshqn6OmLnz32G5ayop1KTodkjsnOUbuooXww9Uu'
    };

    var classifyApiBaseUrl = 'https://viktorstaikov.pythonanywhere.com/api';
    var heroClasses = [
      'Druid',
      'Hunter',
      'Mage',
      'Paladin',
      'Priest',
      'Rogue',
      'Shaman',
      'Warlock',
      'Warrior'
    ];

    var prepareSuggestions = function(data) {
      displayData = [];
      for (i in data) {
        displayData.push({
          display: data[i].name,
          value: data[i].name
        });
      }

      return displayData;
    };

    $scope.getCardSuggestions = function() {
      return $http({
        method: 'GET',
        url: hearthstoneApiBaseUrl + '/cards/search/' + $scope.searchCardText,
        headers: hearthstoneApiHeaders
      }).then(function success(response) {
          return prepareSuggestions(response.data);
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
      $http({
        method: 'POST',
        url: classifyApiBaseUrl + '/deck/classify',
        data: {
          hero_class: $scope.heroClass,
          deck: $scope.deck
        }
      }).then(function success(response) {
        console.log(response);
      });
    };

    var loadImage = function(card) {
      $http({
        method: 'GET',
        url: hearthstoneApiBaseUrl + '/cards/' + card,
        headers: hearthstoneApiHeaders
      }).then(function success(response) {
        var cardIndex = getCardIndex(card);
        if (cardIndex != -1) {
          $scope.deck[cardIndex]['img'] = response.data[0]['img'];
        }
      });
    };

    $scope.addToDeck = function() {
      if (!$scope.selectedCard) {
        return;
      }

      var card =  $scope.selectedCard.value
      var cardIndex = getCardIndex(card);

      if (cardIndex !== -1) {
        $scope.deck[cardIndex]['card-count'] += 1;
      } else {
        $scope.deck.push({
          'card-name': card,
          'card-count': 1,
          'img': 'card-back-default.png'
        });

        loadImage(card);
      }

      $scope.searchCardText = '';
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

      updateClassifier();
    };

    $scope.getHeroClassSuggestions = function () {
      var prefix = $scope.searchHeroClassText.toLowerCase();
      var suggestions = [];
      for (i in heroClasses) {
        if (heroClasses[i].toLowerCase().startsWith(prefix)) {
          suggestions.push({
            display: heroClasses[i],
            value: heroClasses[i]
          });
        }
      }

      return suggestions;
    };

    $scope.displayedRows = [];
    $scope.deck = [];
    $scope.heroClass = '';
  }]);
