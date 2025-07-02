def getParametersWithOverrides(String yamlFilePath, Map jenkinsParams) {
  def finalParams = [:]

  // Default values
  def defaultValues = [
        logLevel: 'TRACE',
        libPath: './resources:./data:./lib:./tests',
        xunitReport: 'xunit.xml',
        reportOutputDir: './reports',
        environment: 'INT_XYZ',
        mode: '',
        org: '1A',
        testfolder: './tests',
        emailRecipients: '',
        credentialID: 'robot_sample_creds',
        cronTrigger: ''
    ]

  // Load parameters from YAML file if it exists
  def yamlParams = [:]
  if (yamlFilePath && yamlFilePath.trim()) {
    try {
      def yamlText = readFile(yamlFilePath)
      if (yamlText && yamlText.trim()) {
        yamlParams = readYaml(text: yamlText)
        echo "Loaded parameters from YAML file: ${yamlFilePath}"
      } else {
        echo "YAML file exists but is empty: ${yamlFilePath}"
      }
    } catch (Exception e) {
      echo "Warning: Could not read YAML file: ${e.message}"
    }
  } else {
    echo 'No YAML file path provided, using Jenkins parameters and defaults only'
  }

  // Jenkins params > YAML params > Default values
  defaultValues.each { paramName, defaultValue ->
        // check if Jenkins parameter exists and is not empty
        if (jenkinsParams.containsKey(paramName) && jenkinsParams[paramName] != null && jenkinsParams[paramName].toString().trim() != '') {
      finalParams[paramName] = jenkinsParams[paramName]
      echo "Using Jenkins parameter for ${paramName}: ${finalParams[paramName]}"
        }
        //check if YAML parameter exists
        else if (yamlParams.params.containsKey(paramName) && yamlParams.params[paramName] != null && yamlParams.params[paramName].toString().trim() != '') {
      finalParams[paramName] = yamlParams.params[paramName]
      echo "Using YAML file parameter for ${paramName}: ${finalParams[paramName]}"
        }
        // fall back to default
        else {
      finalParams[paramName] = defaultValue
      echo "Using default value for ${paramName}: ${finalParams[paramName]}"
        }
  }
  println "Final parameters: ${finalParams}"

  return finalParams
}

def getScheduler(scheduleParam) {
  def scheduleParameter =  scheduleParam as String[]
  println('Schedule Param:' + scheduleParameter)
  def scheduler = ''
  for (schedulerStr in scheduleParameter) {
    println('scheduler Info:    ' + schedulerStr)
    scheduler += schedulerStr + '\n'
  }

  return scheduler
}

def getCredentials(mode, credentialID) {
  echo "Running in mode: ${mode}"
  if (mode != 'mock' && mode != 'cyberark') {
    echo 'Using credentials for authentication'
    withCredentials([usernamePassword(credentialsId: credentialID,
                                                         usernameVariable: 'USERNAME',
                                                         passwordVariable: 'PASSWORD')]) {
      // Update the credentials for use in subsequent stages
      env.user = USERNAME
      env.pwd = PASSWORD
      echo "Credentials have been set for ${environment} environment"
      echo "Username: ${user}"
                                                         }
                    } else {
    echo "Using configured credentials for ${mode} mode"
  }
}
return this
