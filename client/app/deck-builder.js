var deckBuilder = angular.module('deck-builder', ['ngMaterial', 'smart-table', 'chart.js'])
  .controller('DeckController', ['$scope', '$http', function($scope, $http) {
    // Utility
   var getCardIndex = function(cardName, deck) {
      for (i in deck) {
        if (deck[i]['card_name'] === cardName) {
          return i;
        }
      }

      return -1;
    };

    // Chart
    $scope.archetypeNames = [];
    $scope.archetypePercent = [];

    var initChart = function(archetypes) {
      var archetypeNames = Object.keys(archetypes);
      $scope.archetypeNames = archetypeNames;

      $scope.archetypePercent = [];
      for (i in archetypeNames) {
        $scope.archetypePercent.push(archetypes[archetypeNames[i]]);
      }
    };

    // Decks table
    $scope.displayedNearest = [];
    $scope.nearest = [];

    var initDecksTable = function(data) {
      $scope.nearest = [];

      for (i in data) {
        var cards_match = 30 - data[i][0];
        var deckData = data[i][1];

        $scope.nearest.push({
          archetype: deckData['archetype'],
          cards_match: cards_match,
          title: deckData['deck'][0]['title']
        });
      }
    };

    // Lefto to play section
    $scope.previewDeck = '';
    $scope.displayedPreviewDeck = [];
    $scope.previewDeckCards = [];
    var initDeckPreview = function(deck) {
      $scope.previewDeck = deck[0].title;
      $scope.previewDeckCards.splice(0, $scope.previewDeckCards.length);

      for (i in deck) {
        var cardIndex = getCardIndex(deck[i].card_name, $scope.deck);
        var cardCount = 0;
        if (cardIndex == -1) {
          cardCount = deck[i].card_count
        } else {
          cardCount = $scope.deck[cardIndex]['card_count'] - deck[i]['card_count'];
        }

        $scope.previewDeckCards.push({
          card_name: deck[i].card_name,
          card_count: cardCount
        });
      }
    }

    // Classification
    var classifyApiBaseUrl = 'https://viktorstaikov.pythonanywhere.com/api';

    var updateClassifier = function() {
      $http({
        method: 'POST',
        url: classifyApiBaseUrl + '/deck/classify',
        data: {
          hero_class: $scope.heroClass.value,
          deck: $scope.deck
        }
      }).then(function success(response) {
        initChart(response.data['archetypes']);
        initDecksTable(response.data['nearest']);
        initDeckPreview(response.data['nearest'][0][1]['deck']);
      });
    };

    // Autocomplete add card
    var hearthstoneApiBaseUrl = 'https://omgvamp-hearthstone-v1.p.mashape.com';
    var hearthstoneApiHeaders = {
      'X-Mashape-Key': 'MQ5WRXL3ZEmshqn6OmLnz32G5ayop1KTodkjsnOUbuooXww9Uu'
    };

    var prepareSuggestions = function(data) {
      if (!$scope.heroClass) {
        return [];
      }

      displayData = [];
      for (i in data) {
        if (data[i].playerClass == $scope.heroClass.value || !data[i].playerClass) {
          displayData.push({
            display: data[i].name,
            value: data[i].name
          });
        }
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

    // Autocomplete for hero class
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

    $scope.selectHeroClass = function() {
      $scope.deck.splice(0, $scope.deck.splice.length);
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

    // Deck view
    var loadImage = function(card) {
      $http({
        method: 'GET',
        url: hearthstoneApiBaseUrl + '/cards/' + card,
        headers: hearthstoneApiHeaders
      }).then(function success(response) {
        var cardIndex = getCardIndex(card, $scope.deck);
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
      var cardIndex = getCardIndex(card, $scope.deck);

      if (cardIndex !== -1) {
        $scope.deck[cardIndex]['card_count'] += 1;
      } else {
        $scope.deck.push({
          'card_name': card,
          'card_count': 1,
          'img': 'card-back-default.png'
        });

        loadImage(card);
      }

      $scope.searchCardText = '';
      updateClassifier();
    };

    $scope.removeFromDeck = function(card) {
      cardIndex = getCardIndex(card['card_name'], $scope.deck);
      if (cardIndex === -1) {
        return;
      }

      $scope.deck[cardIndex]['card_count']--;
      if ($scope.deck[cardIndex]['card_count'] <= 0) {
        $scope.deck.splice(cardIndex, 1);
      }

      updateClassifier();
    };

    $scope.displayedDeck = [];
    $scope.deck = [];
  }]);
