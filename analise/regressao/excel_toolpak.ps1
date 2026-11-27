# Roda a Análise de Dados do Excel (Analysis ToolPak - VBA) por automação COM.
# Uso: pwsh -File excel_toolpak.ps1 -Plano <arquivo.json>
# O plano JSON lista, por pasta de trabalho, as ferramentas a rodar e onde colocar a saída.
# Segurança: cria uma instância própria do Excel e encerra só ela; nunca toca em Excel que já estava aberto.
param([Parameter(Mandatory = $true)][string]$Plano, [int]$LimiteSeg = 900, [string]$Janelas = '', [string]$SaidaJanelas = '')

$ErrorActionPreference = 'Stop'
$cfg = Get-Content -Raw -LiteralPath $Plano | ConvertFrom-Json
$antes = @(Get-Process EXCEL -ErrorAction SilentlyContinue | ForEach-Object Id)
$xl = New-Object -ComObject Excel.Application
$novo = @(Get-Process EXCEL -ErrorAction SilentlyContinue | ForEach-Object Id | Where-Object { $antes -notcontains $_ })
"PID_NOVO=$($novo -join ',')"
$M = [System.Reflection.Missing]::Value
# vigia: se a automação pendurar (caixa de diálogo modal), registra as janelas abertas e encerra SÓ a instância nova
$vigia = Start-Job -ArgumentList $novo, $LimiteSeg, $Janelas, $SaidaJanelas -ScriptBlock {
    param($pids, $lim, $jan, $saida)
    Start-Sleep -Seconds $lim
    foreach ($p in $pids) {
        if ($jan) { & $jan -ProcId $p -Saida $saida }
        Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
    }
}
try {
    $xl.Visible = $false
    $xl.DisplayAlerts = $false
    $xl.ScreenUpdating = $false
    # carrega o suplemento VBA da Análise de Dados (não carrega sozinho em automação)
    $atp = $null
    foreach ($a in $xl.AddIns) { if ($a.FullName -like '*ATPVBAEN.XLAM') { $atp = $a } }
    if (-not $atp) { throw 'ATPVBAEN.XLAM (Analysis ToolPak - VBA) não encontrado' }
    foreach ($a in $xl.AddIns) { if ($a.FullName -like '*ANALYS32.XLL') { $null = $xl.RegisterXLL($a.FullName); "XLL=$($a.FullName)" } }
    $null = $xl.Workbooks.Open($atp.FullName)
    try { $null = $xl.Run('ATPVBAEN.XLAM!auto_open') } catch { "auto_open indisponível" }
    "ATP=$($atp.FullName)"
    foreach ($job in $cfg.pastas) {
        $wb = $xl.Workbooks.Open($job.arquivo)
        foreach ($t in $job.tarefas) {
            $src = $wb.Worksheets.Item($t.aba_dados)
            $out = $null
            foreach ($s in $wb.Worksheets) { if ($s.Name -eq $t.aba_saida) { $out = $s } }
            if (-not $out) { $out = $wb.Worksheets.Add([Type]::Missing, $wb.Worksheets.Item($wb.Worksheets.Count)); $out.Name = $t.aba_saida }
            $dest = $out.Range('A1')
            switch ($t.ferramenta) {
                'Regress' {
                    # Regress(Y, X, constante_zero, rótulos, confiança, saída, resíduos, resíduos padronizados,
                    #         plotagem de resíduos, plotagem de ajuste, saída em nova planilha, plotagem normal)
                    $null = $xl.Run('ATPVBAEN.XLAM!Regress', $src.Range($t.y), $src.Range($t.x), $false, $true, $M, $dest, $false, $false, $false, $false, $M, $false)
                }
                'Anova1' {
                    $null = $xl.Run('ATPVBAEN.XLAM!Anova1', $src.Range($t.entrada), $dest, 'C', $true, 0.05)
                }
                'Formulas' { }
                default {
                    # testes t de duas amostras (nomes internos do ATPVBAEN, conferidos pela saída):
                    #   Pttestv = "t-Test: Two-Sample Assuming Unequal Variances" (Welch)
                    #   Ttestm  = "t-Test: Two-Sample Assuming Equal Variances" (variância combinada)
                    $null = $xl.Run("ATPVBAEN.XLAM!$($t.ferramenta)", $src.Range($t.entrada1), $src.Range($t.entrada2), $dest, $true, 0.05, 0)
                }
            }
            # caminho B: fórmulas nativas que recalculam o p a partir da estatística e dos gl
            foreach ($f in $t.formulas) { $out.Range($f.celula).Formula = $f.formula }
            "OK $($job.arquivo) :: $($t.aba_saida)"
        }
        $xl.CalculateFull()
        $wb.Save()
        $wb.Close($false)
    }
}
finally {
    Stop-Job $vigia -ErrorAction SilentlyContinue; Remove-Job $vigia -Force -ErrorAction SilentlyContinue
    foreach ($w in @($xl.Workbooks)) { try { $w.Close($false) } catch {} }
    $xl.Quit()
    [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl)
    [GC]::Collect(); [GC]::WaitForPendingFinalizers()
    Start-Sleep -Milliseconds 500
    foreach ($p in $novo) { if (Get-Process -Id $p -ErrorAction SilentlyContinue) { Stop-Process -Id $p -Force; "ENCERRADO_PID=$p" } }
}
