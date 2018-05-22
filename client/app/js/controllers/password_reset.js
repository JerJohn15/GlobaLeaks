GLClient.controller('PasswordResetCtrl', ['$scope', '$location',
  function($scope, $location) {
  // If already logged in, just go to the landing page.
  if ($scope.session !== undefined && $scope.session.auth_landing_page) {
    $location.path($scope.session.auth_landing_page);
  }

  $scope.passwordResetEnabled = $scope.node.enable_password_reset;

}]);
