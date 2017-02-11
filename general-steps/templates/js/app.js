var app = angular.module('Annotate', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

app.controller('annotate', function($scope){
    var annotated = []
    var annotations = {}

    $scope.row_annotation = function row_annotation(row, annotation_type, annotation ){
        annotations[row][annotation] = annotation
    }

    // $scope.annotate = function annotate(positive, negative, neutral){
    //     annotated.push({"positive":positive, "negative":negative, "neutral": neutral })
    // }

    $scope.save = function save(){
        var url = 'data:text/json;charset=utf8,' + encodeURIComponent(JSON.stringify(annotations));
        $window.open(url, '_blank');
    }

})