import os
import sys
import unittest

from click.testing import CliRunner
from subprocess import Popen, DEVNULL, PIPE
from stakkr.docker_clean import clean

base_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, base_dir + '/../')


class DockerCleanTest(unittest.TestCase):
    def test_no_arg(self):
        result = CliRunner().invoke(clean)
        self.assertEqual(0, result.exit_code)
        regex = r'.*Clean Docker stopped containers, images, volumes and networks.*'
        self.assertRegex(result.output, regex)

    def test_bad_arg(self):
        result = CliRunner().invoke(clean, ['hello-world'])
        self.assertEqual(2, result.exit_code)
        self.assertRegex(result.output, r'Usage: docker-clean \[OPTIONS\].*')

    def test_full_clean(self):
        # Stop everything
        cmd = ['docker', 'stop', '$(docker ps -a -q)']
        Popen(cmd, shell=True, stdout=PIPE, stderr=DEVNULL).communicate()
        # We should have things stored
        Popen(['docker', 'volume', 'create', 'hello'], stdout=PIPE, stderr=DEVNULL).communicate()
        vols = Popen(['docker', 'volume', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertGreater(len(vols.splitlines()), 1)

        Popen(
            ['docker', 'network', 'create', '--driver', 'bridge', 'test_delete'],
            stdout=PIPE,
            stderr=DEVNULL).communicate()
        # that one won't be cleaned
        Popen(
            ['docker', 'network', 'create', '--driver', 'bridge', 'network_pytest'],
            stdout=PIPE,
            stderr=DEVNULL).communicate()
        nets = Popen(['docker', 'network', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertGreater(len(nets.splitlines()), 5)

        Popen(['docker', 'run', 'hello-world'], stdout=PIPE, stderr=DEVNULL).communicate()
        # that one won't be cleaned
        Popen(
            ['docker', 'run', '--rm', '--detach', '--name', 'nginx_pytest', 'nginx:stable-alpine'],
            stdout=PIPE,
            stderr=DEVNULL).communicate()
        Popen(
            ['docker', 'network', 'connect', 'network_pytest', 'nginx_pytest'],
            stdout=PIPE,
            stderr=DEVNULL).communicate()
        images = Popen(['docker', 'image', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertGreater(len(images.splitlines()), 1)
        cts = Popen(['docker', 'ps', '-a'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertGreater(len(cts.splitlines()), 2)

        # CLEAN
        result = CliRunner().invoke(clean, ['--force', '--verbose'])
        self.assertEqual(0, result.exit_code)
        regex = r'.*Clean Docker stopped containers, images, volumes and networks.*'
        self.assertRegex(result.output, regex)

        # Make sure it has been cleaned
        nets = Popen(['docker', 'network', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(nets.splitlines()), 5)
        vols = Popen(['docker', 'volume', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(vols.splitlines()), 1)

        # Problem with scrutinizer : can't remove images
        # TODO check and fix it later
        if 'SCRUTINIZER_API_ENDPOINT' not in os.environ:
            images = Popen(['docker', 'image', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
            self.assertIs(len(images.splitlines()), 2)

        cts = Popen(['docker', 'ps', '-a'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(cts.splitlines()), 2)

        # Stop nginx and clean again
        Popen(['docker', 'stop', 'nginx_pytest'], stdout=PIPE, stderr=DEVNULL).communicate()

        CliRunner().invoke(clean, ['--force', '--verbose'])
        # Make sure it has been cleaned
        nets = Popen(['docker', 'network', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(nets.splitlines()), 4)
        vols = Popen(['docker', 'volume', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(vols.splitlines()), 1)

        # Problem with scrutinizer : can't remove images
        # TODO check and fix it later
        if 'SCRUTINIZER_API_ENDPOINT' not in os.environ:
            images = Popen(['docker', 'image', 'ls'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
            self.assertIs(len(images.splitlines()), 1)

        cts = Popen(['docker', 'ps', '-a'], stdout=PIPE, stderr=DEVNULL).communicate()[0]
        self.assertIs(len(cts.splitlines()), 1)


if __name__ == "__main__":
    unittest.main()
