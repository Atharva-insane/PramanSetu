# 🧪 PramanSetu Automated Testing Framework

### How to Run All Test Suites:
```bash
# Run complete test suite via Python 3.14 Pytest runner
py -3.14 -c "
import sys
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\Lib\site-packages')
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI')
sys.path.insert(0, r'C:\Users\LENOVO\OneDrive\Desktop\CivicAudit AI\CivicAudit AI\backend')
import pytest
sys.exit(pytest.main(['backend/tests/', '-v']))
"
```
