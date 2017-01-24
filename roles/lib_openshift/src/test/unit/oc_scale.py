#!/usr/bin/env python2
'''
 Unit tests for oc scale
'''
# To run
# python -m unittest version
#
# .
# Ran 1 test in 0.597s
#
# OK

import mock
import os
import sys
import unittest

# Removing invalid variable names for tests so that I can
# keep them brief
# pylint: disable=invalid-name,no-name-in-module
# Disable import-error b/c our libraries aren't loaded in jenkins
# pylint: disable=import-error
# place class in our python path
module_path = os.path.join('/'.join(os.path.realpath(__file__).split('/')[:-4]), 'library')  # noqa: E501
sys.path.insert(0, module_path)
from oc_scale import OCScale  # noqa: E402


# pylint: disable=unused-argument
def oc_cmd_mock(cmd, oadm=False, output=False, output_type='json', input_data=None):
    '''mock command for openshift_cmd'''
    version = '''oc v3.4.0.39
kubernetes v1.4.0+776c994
features: Basic-Auth GSSAPI Kerberos SPNEGO

Server https://internal.api.opstest.openshift.com
openshift v3.4.0.39
kubernetes v1.4.0+776c994
'''
    if 'version' in cmd:
        return {'stderr': None,
                'stdout': version,
                'returncode': 0,
                'results': version,
                'cmd': cmd}


class OCScaleTest(unittest.TestCase):
    '''
     Test class for OCVersion
    '''

    def setUp(self):
        ''' setup method will create a file and set to known configuration '''
        pass

    @mock.patch('oc_scale.OCScale.openshift_cmd')
    def test_state_list(self, mock_openshift_cmd):
        ''' Testing a get '''
        params = {'name': 'router',
                  'namespace': 'default',
                  'replicas': 2,
                  'state': 'list',
                  'kind': 'dc',
                  'kubeconfig': '/etc/origin/master/admin.kubeconfig',
                  'debug': False}


        dc = '''{"kind": "DeploymentConfig",
               "apiVersion": "v1",
               "metadata": {
                   "name": "router",
                   "namespace": "default",
                   "selfLink": "/oapi/v1/namespaces/default/deploymentconfigs/router",
                   "uid": "a441eedc-e1ae-11e6-a2d5-0e6967f34d42",
                   "resourceVersion": "6558",
                   "generation": 8,
                   "creationTimestamp": "2017-01-23T20:58:07Z",
                   "labels": {
                       "router": "router"
                   }
               },
               "spec": {
                   "replicas": 2,
               }
           }'''


        mock_openshift_cmd.side_effect = [
            {"cmd": '/usr/bin/oc get dc router -n default',
             'results': dc,
             'returncode': 0,
            }
        ]

        results = OCScale.run_ansible(params, False)

        self.assertFalse(results['changed'])
        self.assertEqual(results['result'][0], 2)

    @mock.patch('oc_scale.OCScale.openshift_cmd')
    def test_scale(self, mock_openshift_cmd):
        ''' Testing a get '''
        params = {'name': 'router',
                  'namespace': 'default',
                  'replicas': 3,
                  'state': 'list',
                  'kind': 'dc',
                  'kubeconfig': '/etc/origin/master/admin.kubeconfig',
                  'debug': False}


        dc = '''{"kind": "DeploymentConfig",
               "apiVersion": "v1",
               "metadata": {
                   "name": "router",
                   "namespace": "default",
                   "selfLink": "/oapi/v1/namespaces/default/deploymentconfigs/router",
                   "uid": "a441eedc-e1ae-11e6-a2d5-0e6967f34d42",
                   "resourceVersion": "6558",
                   "generation": 8,
                   "creationTimestamp": "2017-01-23T20:58:07Z",
                   "labels": {
                       "router": "router"
                   }
               },
               "spec": {
                   "replicas": 3,
               }
           }'''


        mock_openshift_cmd.side_effect = [
            {"cmd": '/usr/bin/oc get dc router -n default',
             'results': dc,
             'returncode': 0,
            },
            {"cmd": '/usr/bin/oc create -f /tmp/router -n default',
             'results': '',
             'returncode': 0,
            },
        ]

        results = OCScale.run_ansible(params, False)

        self.assertFalse(results['changed'])
        self.assertEqual(results['result'][0], 3)

    def tearDown(self):
        '''TearDown method'''
        pass


if __name__ == "__main__":
    unittest.main()
