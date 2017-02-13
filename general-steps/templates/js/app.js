var app = angular.module('Annotate', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{a');
  $interpolateProvider.endSymbol('a}');
}]);

app.controller('annotate', function($scope, $window){
    var annotated = []
    var annotations = {}

    var createNestedObject = function( base, names ) {
    for( var i = 0; i < names.length; i++ ) {
        base = base[ names[i] ] = base[ names[i] ] || {};
    }
};

    $scope.row_annotation = function row_annotation(row, annotation_type, annotation ){
        console.log("row", row)
        console.log("annotation_type", annotation_type)
        console.log("annotation", annotation)
        createNestedObject( annotations, [row, annotation_type] );
        annotations[row][annotation_type] = annotation
    }

    // $scope.annotate = function annotate(positive, negative, neutral){
    //     annotated.push({"positive":positive, "negative":negative, "neutral": neutral })
    // }

    $scope.saveToDisk = function (data, filename) {

  if (!data) {
    console.error('No data');
    return;
  }

  if (!filename) {
    filename = 'download.json';
  }

  if (typeof data === 'object') {
    data = JSON.stringify(data, undefined, 2);
  }

  var blob = new Blob([data], {type: 'text/json'});

  // FOR IE:

  if (window.navigator && window.navigator.msSaveOrOpenBlob) {
      window.navigator.msSaveOrOpenBlob(blob, filename);
  }
  else{
      var e = document.createEvent('MouseEvents'),
          a = document.createElement('a');

      a.download = filename;
      a.href = window.URL.createObjectURL(blob);
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':');
      e.initEvent('click', true, false, window,
          0, 0, 0, 0, 0, false, false, false, false, 0, null);
      a.dispatchEvent(e);
  }
};

    $scope.save = function save(){
        $scope.saveToDisk(annotations,'annotations.json')
        // var url = 'data:text/json;charset=utf8,' + encodeURIComponent(JSON.stringify(annotations));
        // $window.open(url, '_blank');

        // $window.focus();
    }

})