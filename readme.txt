˵��

1. ���� python sailingInfoSpider.py beijing ���Բ�ѯ output\beijing Ŀ¼�� url.txt �е�����ɸѡ�б�ҳ���ݡ�
2. url.txt ���� python urlDetector.py beijing ���ɡ�������и�ģʽ�ο� cityConstants.py��
3. ʵ�ʲ���ǰ�������ȵ��� python testUrlCount.txt ����֮ǰ��ɸѡ�����Ƿ��������ɸѡ������� 3000 ����ҳ������ 100���������Ҫ���µ��� url.txt ��֤ÿ�� url �µ�ɸѡ�б��������� 3000 ����
4. ������� worker.py ����������������ڸô����ϣ����Ƴ������� sailingInfoSpider.py ���ݹ����Ĳ�������ȷ���������ĸ� worker ���������ֶ�����ִ�� worker ���ɣ��硰python worker.py https://xxx 3 huairou beijing��
5. ������ worker.py ������ time.sleep(x) ���Ͳ�ѯƵ�ʣ���ֹ���������ܾ���