#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from chibi.file import Chibi_path
from chibi.file.temp import Chibi_temp_path
from chibi_yum_repo import Chibi_yum_repo


class Test_chibi_yum_repo_read( unittest.TestCase ):
    def setUp( self ):
        self.repo = Chibi_path(
            'tests/elastic.repo' ).open( chibi_file_class=Chibi_yum_repo )

    def test_should_work( self ):
        result = self.repo.read()
        self.assertTrue( result )

    def test_read_should_return_a_dict( self ):
        result = self.repo.read()
        self.assertIsInstance( result, dict )

    def test_read_should_return_expected_len( self ):
        result = self.repo.read()
        self.assertEqual( len( result ), 1 )

    def test_read_should_return_key_section( self ):
        result = self.repo.read()
        self.assertIn( 'elasticsearch-7.x', result )

    def test_content_should_be_a_dict( self ):
        result = self.repo.read()
        data = result[ 'elasticsearch-7.x' ]
        self.assertIsInstance( data, dict )

    def test_content_should_have_name( self ):
        result = self.repo.read()
        data = result[ 'elasticsearch-7.x' ]
        self.assertIn( 'name', data )
        self.assertEqual(
            data.name, 'Elasticsearch repository for 7.x packages' )

    def test_content_should_have_baseurl( self ):
        result = self.repo.read()
        data = result[ 'elasticsearch-7.x' ]
        self.assertIn( 'baseurl', data )
        self.assertEqual(
            data.baseurl, 'https://artifacts.elastic.co/packages/7.x/yum' )

    def test_content_should_have_enabled( self ):
        result = self.repo.read()
        data = result[ 'elasticsearch-7.x' ]
        self.assertIn( 'enabled', data )
        self.assertTrue( data.enabled )


class Test_chibi_yum_repo_read_two( unittest.TestCase ):
    def setUp(self):
        self.repo = Chibi_path(
            'tests/two.repo' ).open( chibi_file_class=Chibi_yum_repo )

    def test_should_work(self):
        result = self.repo.read()
        self.assertTrue( result )

    def test_read_should_return_a_dict( self ):
        result = self.repo.read()
        self.assertIsInstance( result, dict )

    def test_read_should_return_expected_len( self ):
        result = self.repo.read()
        self.assertEqual( len( result ), 2 )

    def test_read_should_return_key_section( self ):
        result = self.repo.read()
        self.assertIn( 'elasticsearch-7.x', result )
        self.assertIn( 'kibana-7.x', result )

    def test_all_contents_should_be_dicts( self ):
        result = self.repo.read()
        for k, v in result.items():
            self.assertIsInstance( v, dict )


class Test_chibi_yum_repo_write( unittest.TestCase ):
    def setUp( self ):
        self.tmp = Chibi_temp_path()
        self.repo_path = Chibi_path( 'tests/elastic.repo' )
        self.tmp_repo = self.repo_path.copy( self.tmp )
        self.repo = self.tmp_repo.open( chibi_file_class=Chibi_yum_repo )

    def test_should_work( self ):
        result = self.repo.read()
        self.assertTrue( result )

    def test_overwrite_name_should_work( self ):
        repo = self.repo.read()
        repo[ 'elasticsearch-7.x' ].name = "asdf"
        self.repo.write( repo )
        new_repo = self.repo.read()
        result_name = new_repo[ 'elasticsearch-7.x' ].name
        self.assertEqual( result_name, "asdf" )


class Test_chibi_yum_repo_write_two( unittest.TestCase ):
    def setUp( self ):
        self.tmp = Chibi_temp_path()
        self.repo_path = Chibi_path( 'tests/two.repo' )
        self.tmp_repo = self.repo_path.copy( self.tmp )
        self.repo = self.tmp_repo.open( chibi_file_class=Chibi_yum_repo )

    def test_should_work( self ):
        result = self.repo.read()
        self.assertTrue( result )

    def test_overwrite_name_should_work( self ):
        repo = self.repo.read()
        repo[ 'elasticsearch-7.x' ].name = "asdf"
        kibana_name = repo[ 'kibana-7.x' ].name
        self.repo.write( repo )
        new_repo = self.repo.read()
        result_name = new_repo[ 'elasticsearch-7.x' ].name
        result_kibana_name = new_repo[ 'kibana-7.x' ].name
        self.assertEqual( result_name, "asdf" )
        self.assertEqual( result_kibana_name, kibana_name )
