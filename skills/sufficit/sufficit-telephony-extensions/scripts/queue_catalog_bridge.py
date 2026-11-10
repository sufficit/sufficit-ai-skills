#!/usr/bin/python3
"""Fleet agent catalog bridge: fixed service and deployment actor; conditional queue/member writes."""
import json,re,sys,uuid,urllib.request,urllib.error,shlex
from pathlib import Path
def guid(v):
 x=uuid.UUID(str(v));assert x.int,'empty UUID';return x.hex
def prepare(d, actor):
 method=d.get('method','GET').upper();assert method in ('GET','PUT'),'GET or PUT required'
 context=guid(d['contextId']);path='/api/queue/contexts/'+context+'/queues'
 if d.get('queueId'):path+='/'+guid(d['queueId'])
 if d.get('members') or d.get('memberId'):
  assert d.get('queueId'),'queueId required';path+='/members'
 if d.get('memberId'):path+='/'+guid(d['memberId'])
 headers={'X-Queue-Actor':guid(actor),'Accept':'application/json'};body=None
 if method=='PUT':
  assert d.get('queueId'),'queueId required'
  assert not d.get('members') or d.get('memberId'),'memberId required for member writes'
  create=d.get('create',False);assert type(create) is bool,'create must be boolean'
  if create:
   assert not d.get('revision'),'creation cannot include a revision'
   resource=uuid.UUID(guid(d.get('memberId') or d['queueId']))
   assert resource.version==7,'new resource requires a stable UUIDv7'
   headers['If-None-Match']='*'
  else:
   revision=d.get('revision','');assert re.fullmatch(r'"[0-9a-fA-F]{32}"',revision),'strong revision required'
   headers['If-Match']=revision
  edit=d['body'];assert isinstance(edit,dict),'body object required'
  if d.get('memberId'):
   allowed={'extension','paused','enabled','dynamic','loggedIn','pauseReason','resetAutoPause','dispatchOrder','agentContextId','penalty'}
   assert set(edit)<=allowed and {'extension','paused','enabled'}<=set(edit),'invalid member fields'
   assert isinstance(edit['extension'],str) and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,31}',edit['extension']),'invalid extension'
   assert type(edit['paused']) is bool and type(edit['enabled']) is bool,'invalid flags'
   if edit.get('agentContextId'):assert guid(edit['agentContextId'])==context,'member must belong to this customer'
   if create:assert edit.get('agentContextId') and guid(edit['agentContextId'])==context,'creation requires same-customer agentContextId'
  else:
   allowed={'title','maxWaitSeconds','maxWaiting','enabled','destination','options'}
   assert set(edit)<=allowed and {'title','maxWaitSeconds','maxWaiting','enabled','destination','options'}<=set(edit),'complete queue policy required'
   assert isinstance(edit['title'],str) and 1<=len(edit['title'].strip())<=100,'invalid queue title'
   assert type(edit['enabled']) is bool and isinstance(edit['options'],dict),'invalid queue flags/options'
   for field in ['maxWaitSeconds','maxWaiting']:assert type(edit[field]) is int and edit[field]>=0,'invalid queue capacity/wait'
  headers['Content-Type']='application/json';body=json.dumps(edit).encode()
 return method,path,headers,body
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args,**kwargs):return None

def main(actor):
 try:
  raw=sys.stdin.buffer.read(32769);assert len(raw)<=32768,'request too large'
  method,path,headers,body=prepare(json.loads(raw), actor)
  env={}
  for line in Path('/etc/sufficit-queue-portal/nodes.env').read_text().splitlines():
   if line and not line.startswith('#'):
    k,v=line.split('=',1);env[k]=shlex.split(v)[0]
  prefix='Sufficit__Telephony__Queue__Catalog__';base=env[prefix+'BaseUrl'].rstrip('/')
  assert base=='http://172.19.2.104:18189','catalog authority changed; review connection'
  headers['Authorization']='Bearer '+Path(env[prefix+'KeyFile']).read_text().strip()
  req=urllib.request.Request(base+path,data=body,headers=headers,method=method)
  try:
   response=urllib.request.build_opener(NoRedirect).open(req,timeout=30)
  except urllib.error.HTTPError as e:response=e
  with response:
   raw=response.read(1048577);assert len(raw)<=1048576,'response too large'
   try:data=json.loads(raw) if raw else None
   except ValueError:data={'error':'non-json response omitted'}
   print(json.dumps({'status':response.code,'data':data}));return 0 if 200<=response.code<300 else 1
 except (ValueError,KeyError,AssertionError,TypeError) as e:
  print(json.dumps({'status':400,'error':str(e)}));return 1
 except Exception as e:
  print(json.dumps({'status':502,'error':type(e).__name__}));return 1
if __name__=='__main__':
 assert len(sys.argv)==2,'deployment must provide its fixed actor GUID'
 sys.exit(main(sys.argv[1]))
