GLClient.controller('ResetPasswordCtrl', ['$scope', '$location',
  function($scope, $location) {
  // If already logged in, just go to the landing page.
  if ($scope.session !== undefined && $scope.session.auth_landing_page) {
    $location.path($scope.session.auth_landing_page);
  }
}]);
