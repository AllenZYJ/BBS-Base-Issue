angular
    .module('materialApp', ['ngMaterial'])
    .controller('AppCtrl', function($scope) {
        $scope.cards = [{
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }, {
            text: 'Bla bla bla bla bla bla bla ',
            title: 'Bla'
        }];
        $scope.displayContent = true;
        $scope.toggleContent = function(showContent) {
            $scope.displayContent = showContent;
        };
    });