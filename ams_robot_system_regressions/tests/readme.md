# **AMS Robot Regression Test Suite Levels**
The structure of the tests is split into multiple "Levels", with each Level run sequentially up to the Max Level for that
environment, unless any test within a Level fails, then the next Level will not be executed. This is to ensure a hierarchy
of very simple to very complex tests with a fail-early mechanism to not bother executing the complex tests if a basic test
does not pass.

