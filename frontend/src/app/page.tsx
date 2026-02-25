import { AgentMatrix } from '../components/portal/agent-matrix';
import { AppShell } from '../components/shell/app-shell';

export default function PortalPage(): JSX.Element {
  return (
    <AppShell
      section="PORTAL"
      title="Matrix Navigation"
      subtitle="Choose an epistemic posture and functional role to route into WORKBENCH or PIPELINE."
    >
      <AgentMatrix />
    </AppShell>
  );
}
