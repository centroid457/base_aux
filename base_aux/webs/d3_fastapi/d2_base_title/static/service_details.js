document.addEventListener('DOMContentLoaded', function() {
    const detailsContent = document.getElementById('service_details-content');
    if (!detailsContent) return;

    function getClientInfo() {
        const ua = navigator.userAgent;
        let browser = "Unknown", os = "Unknown";
        if (ua.includes("Firefox")) browser = "Firefox";
        else if (ua.includes("Edg")) browser = "Edge";
        else if (ua.includes("Chrome")) browser = "Chrome";
        else if (ua.includes("Safari")) browser = "Safari";

        if (ua.includes("Windows NT")) os = "Windows";
        else if (ua.includes("Mac OS X")) os = "macOS";
        else if (ua.includes("Linux")) os = "Linux";
        else if (ua.includes("Android")) os = "Android";
        else if (ua.includes("iPhone") || ua.includes("iPad")) os = "iOS";

        return {
            browser, os,
            user_agent: ua,
            local_time: new Date().toLocaleString()
        };
    }

    function renderDetails(data, container, level = 0) {
        if (!data) return '';
        let html = '';
        const indent = level * 20;

        for (const [key, value] of Object.entries(data)) {
            if (value && typeof value === 'object' && !Array.isArray(value)) {
                html += `<div style="margin-left: ${indent}px; margin-top: 8px;">`;
                html += `<h4 style="margin:0 0 4px 0; color:#2c3e50;">🔹 ${key}</h4>`;
                html += renderDetails(value, null, level + 1);
                html += `</div>`;
            } else {
                html += `
                    <div style="display:flex; margin-left:${indent}px; gap:10px;">
                        <div style="font-weight:bold; min-width:120px;">${key}:</div>
                        <div>${value ?? '—'}</div>
                    </div>
                `;
            }
        }
        if (container) container.innerHTML = html;
        return html;
    }

    async function loadDetails() {
        try {
            const response = await fetch('/api/info');
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const serverData = await response.json();

            const clientInfo = getClientInfo();
            serverData.CLIENT = {
                ip: serverData.NETWORK?.client_ip || 'N/A',
                browser: clientInfo.browser,
                os: clientInfo.os,
                local_time: clientInfo.local_time,
                user_agent: clientInfo.user_agent
            };

            renderDetails(serverData, detailsContent);
        } catch (error) {
            console.error(error);
            detailsContent.innerHTML = `Ошибка: ${error.message}`;
        }
    }

    loadDetails();
});