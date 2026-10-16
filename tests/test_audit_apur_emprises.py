"""Aggregate-only Apur audit contracts, with fake responses and no network."""
import importlib.util
from pathlib import Path
import unittest

path=Path(__file__).resolve().parents[1]/"scripts/audit_apur_emprises.py"
spec=importlib.util.spec_from_file_location("apur_bati_audit",path)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class ApurAuditTests(unittest.TestCase):
    def layer(self):
        return {
            "name":"Période de construction", "geometryType":"esriGeometryPolygon",
            "extent":{"spatialReference":{"latestWkid":2154}},
            "capabilities":"Map,Query,Data",
            "advancedQueryCapabilities":{"supportsStatistics":True},
            "fields":[{"name":f} for f in mod.REQUIRED_FIELDS],
        }

    def counts(self):
        return {"total":10,"median_height_null":1,"median_height_zero":1,
                "median_height_negative":0,"median_height_over_200":0,
                "year_of_construction_null":5,"period_of_construction_null":1,
                "period_undated":2}

    def test_expected_schema_and_units(self):
        self.assertTrue(mod.validate_layer(self.layer()))
        self.assertIn("h_med",mod.REQUIRED_FIELDS)
        self.assertIn("an_const",mod.REQUIRED_FIELDS)
        self.assertNotIn("H_ET_MAX",mod.REQUIRED_FIELDS)

    def test_reject_missing_height_field(self):
        layer=self.layer()
        layer["fields"]=[f for f in layer["fields"] if f["name"]!="h_med"]
        with self.assertRaisesRegex(ValueError,"schema"):
            mod.validate_layer(layer)

    def test_reject_wrong_crs(self):
        layer=self.layer()
        layer["extent"]["spatialReference"]["latestWkid"]=4326
        with self.assertRaisesRegex(ValueError,"2154"):
            mod.validate_layer(layer)

    def test_validate_consistent_aggregate_counts(self):
        self.assertTrue(mod.validate_counts(self.counts(),{None:1,99:2,1:7},
                                            {"min_h_med":0,"max_h_med":25}))

    def test_reject_incompatible_period_totals(self):
        with self.assertRaisesRegex(ValueError,"group counts"):
            mod.validate_counts(self.counts(),{None:1,99:2,1:6},{"min_h_med":0,"max_h_med":25})

    def test_reject_impossible_null_count(self):
        counts=self.counts();counts["year_of_construction_null"]=11
        with self.assertRaisesRegex(ValueError,"Invalid count"):
            mod.validate_counts(counts,{None:1,99:2,1:7},
                                {"min_h_med":0,"max_h_med":25})

    def test_reject_negative_height_and_missing_bounds(self):
        with self.assertRaisesRegex(ValueError,"Impossible height"):
            mod.validate_counts(self.counts(),{None:1,99:2,1:7},
                                {"min_h_med":-1,"max_h_med":50})
        with self.assertRaisesRegex(ValueError,"Missing height"):
            mod.validate_counts(self.counts(),{None:1,99:2,1:7},
                                {"min_h_med":0})

    def test_no_primitive_object_or_geometry_query(self):
        observed=[]
        data=self.counts()
        def fake(url,params):
            observed.append((url,params))
            if url==mod.LAYER_URL:
                return self.layer()
            if "returnCountOnly" in params:
                return {"count":data[next(k for k,v in mod.COUNT_WHERE.items()
                                       if v==params["where"])]}
            if "groupByFieldsForStatistics" in params:
                return {"features":[{"attributes":{"c_perconst":None,"n":1}},
                                    {"attributes":{"c_perconst":99,"n":2}},
                                    {"attributes":{"c_perconst":1,"n":7}}]}
            return {"features":[{"attributes":{"min_h_med":0,"max_h_med":25}}]}
        result=mod.audit(query=fake)
        self.assertEqual(result["objects"],10)
        self.assertEqual(result["eligible_positive_median_height_count"],8)
        self.assertEqual(result["dated_period_count"],7)
        self.assertTrue(all(p.get("returnGeometry")=="false" or p.get("returnCountOnly")=="true"
                            for _,p in observed if "query" in _))
        self.assertEqual(len(observed),11)

if __name__=="__main__":
    unittest.main()
