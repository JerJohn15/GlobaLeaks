GLClient.controller('PasswordResetCtrl', ['$scope', '$location', '$http',
  function($scope, $location, $http) {
  // If already logged in, just go to the landing page.
  if ($scope.session !== undefined && $scope.session.auth_landing_page) {
    $location.path($scope.session.auth_landing_page);
  }

  $scope.resetCredentials = {
    'username': '',
    'mail_address': '',
  };

  var completed = false;

  $scope.passwordResetEnabled = $scope.node.enable_password_reset;

  $scope.complete = function() {
    $http.post('reset/password', $scope.resetCredentials)
  }
}]);
