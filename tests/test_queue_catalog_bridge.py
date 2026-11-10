import importlib.util
import json
import unittest
from pathlib import Path

path=Path(__file__).resolve().parents[1]/'skills/sufficit/sufficit-telephony-extensions/scripts/queue_catalog_bridge.py'
spec=importlib.util.spec_from_file_location('catalog_bridge',path);bridge=importlib.util.module_from_spec(spec);spec.loader.exec_module(bridge)
CONTEXT='a85434ee136542f09b07c59da6b1b791'
QUEUE='019a6b1a12347abc8def123456789abc'
MEMBER='019a6b1a12347abc8def123456789abd'
ACTOR='01a17db20bd87641855666c5b41ba062'
class QueueBridgeTests(unittest.TestCase):
 def queue(self):return {'method':'PUT','contextId':CONTEXT,'queueId':QUEUE,'create':True,'body':{'title':'Principal','maxWaitSeconds':45,'maxWaiting':20,'enabled':True,'destination':'','options':{}}}
 def member(self):return {'method':'PUT','contextId':CONTEXT,'queueId':QUEUE,'memberId':MEMBER,'create':True,'body':{'extension':'0001336001','paused':False,'enabled':True,'agentContextId':CONTEXT,'penalty':0}}
 def test_create_requires_conditional_insert_and_fixed_actor(self):
  for d in [self.queue(),self.member()]:
   method,path,h,body=bridge.prepare(d,ACTOR);self.assertEqual(method,'PUT');self.assertEqual(h['If-None-Match'],'*');self.assertNotIn('If-Match',h);self.assertEqual(h['X-Queue-Actor'],ACTOR);self.assertEqual(json.loads(body),d['body']);self.assertTrue(path.startswith('/api/queue/contexts/'+CONTEXT+'/queues/'+QUEUE))
 def test_update_requires_exact_revision_and_preserves_body(self):
  d=self.member();d.pop('create');d['revision']='"'+MEMBER+'"';method,path,h,body=bridge.prepare(d,ACTOR);self.assertEqual(h['If-Match'],d['revision']);self.assertNotIn('If-None-Match',h);self.assertEqual(json.loads(body),d['body'])
 def test_rejects_unconditional_writes_reused_non_v7_ids_and_mixed_conditions(self):
  for mutate in [lambda d:d.pop('create'),lambda d:d.update(queueId=CONTEXT),lambda d:d.update(revision='"'+MEMBER+'"'),lambda d:d.update(method='DELETE'),lambda d:d.update(create='true')]:
   d=self.queue();mutate(d)
   with self.assertRaises(AssertionError):bridge.prepare(d,ACTOR)
 def test_cross_customer_membership_and_missing_policy_are_rejected(self):
  d=self.member();d['body']['agentContextId']=MEMBER
  with self.assertRaises(AssertionError):bridge.prepare(d,ACTOR)
  d=self.queue();d['body'].pop('options')
  with self.assertRaises(AssertionError):bridge.prepare(d,ACTOR)
 def test_get_and_historical_member_edit_remain_supported(self):
  method,path,h,body=bridge.prepare({'contextId':CONTEXT,'queueId':QUEUE,'members':True},ACTOR);self.assertEqual(method,'GET');self.assertTrue(path.endswith('/members'));self.assertIsNone(body)
  d=self.member();d.pop('create');d['revision']='"'+MEMBER+'"';d['body'].pop('agentContextId');bridge.prepare(d,ACTOR)
if __name__=='__main__':unittest.main()
