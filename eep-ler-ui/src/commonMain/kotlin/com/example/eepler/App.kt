package com.example.eepler

import androidx.compose.foundation.background
import androidx.compose.foundation.isSystemInDarkTheme // For dark theme
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.compose.material3.Button

// This will be the main Composable for your application's UI
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun App(useDarkTheme: Boolean, onThemeToggle: () -> Unit) { // Accept dark theme state and toggle function
    val colors = if (useDarkTheme) {
        darkColorScheme()
    } else {
        lightColorScheme()
    }

    MaterialTheme(
        colorScheme = colors
    ) {
        Surface(modifier = Modifier.fillMaxSize()) {
            Column { // Add a column to hold the button and the interface
                Button(onClick = onThemeToggle, modifier = Modifier.padding(8.dp)) {
                    Text(if (useDarkTheme) "Switch to Light Theme" else "Switch to Dark Theme")
                }
                MainAnalysisInterface() // Your existing interface
            }
        }
    }
}

@Composable
fun MainAnalysisInterface() {
    Column(modifier = Modifier.fillMaxSize()) {
        // 1. Query Input Panel (Top, 20% of screen height)
        QueryInputPanel(modifier = Modifier.weight(0.25f).fillMaxWidth()) // Adjusted weight slightly for more space

        // 2. Results Dashboard (Center, 60% of screen height)
        ResultsDashboard(modifier = Modifier.weight(0.60f).fillMaxWidth())

        // 3. Status Bar (Bottom, 10% of screen height)
        StatusBar(modifier = Modifier.weight(0.15f).fillMaxWidth()) // Adjusted weight slightly
    }
}

// Data classes for the Mathematical Engine dropdown options
sealed class EngineOption {
    data class Header(val title: String) : EngineOption()
    data class SubHeader(val title: String) : EngineOption()
    data class Item(val displayName: String, val id: String, val enabled: Boolean) : EngineOption()
}

@OptIn(ExperimentalMaterial3Api::class) // Needed for ExposedDropdownMenuBox
@Composable
fun QueryInputPanel(modifier: Modifier = Modifier) {
    var phenomenonText by remember { mutableStateOf("") }
    var selectedEep by remember { mutableStateOf("Distributed Intelligence") } // Placeholder
    var analysisDepth by remember { mutableStateOf("Standard") } // Placeholder
    var isLoading by remember { mutableStateOf(false) }

    // Data for the Mathematical Engine dropdown
    val engineOptions = remember { // Use remember to avoid recreating the list on every recomposition
        listOf(
            EngineOption.Header("Available Now"),
            EngineOption.Item("Python SciPy (Free, Powerful)", "python_scipy", true),
            EngineOption.Item("Browser Native (Free, Fast)", "browser_native", true),
            EngineOption.Header("Future Premium Options (Ghosted)"),
            EngineOption.SubHeader("Premium Engines (Coming Soon):"),
            EngineOption.Item("MATLAB Online (License Required)", "matlab_online", false),
            EngineOption.Item("Mathematica Cloud (Symbolic Computing)", "mathematica_cloud", false),
            EngineOption.Item("Intel MKL (5-10x Performance)", "intel_mkl", false),
            EngineOption.Item("Maple (Advanced Symbolic)", "maple_cloud", false),
            EngineOption.Item("NAG Library (High Precision)", "nag_library", false),
            EngineOption.Header("Enterprise Tier (Ultra-Ghosted)"),
            EngineOption.SubHeader("Enterprise Tier (Future):"),
            EngineOption.Item("Wolfram Enterprise", "wolfram_enterprise", false),
            EngineOption.Item("Local MATLAB Integration", "matlab_local", false),
            EngineOption.Item("Custom HPC Cluster", "custom_hpc", false)
        )
    }
    // Find the first enabled item to be the default selection
    val defaultEngine = remember { engineOptions.filterIsInstance<EngineOption.Item>().firstOrNull { it.enabled } }
    var selectedEngine by remember { mutableStateOf(defaultEngine) }
    var engineDropdownExpanded by remember { mutableStateOf(false) }


    Column(
        modifier = modifier
            .padding(16.dp)
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
        verticalArrangement = Arrangement.spacedBy(8.dp) // Consistent spacing
    ) {
        OutlinedTextField(
            value = phenomenonText,
            onValueChange = { phenomenonText = it },
            label = { Text("Analyze phenomenon:") },
            modifier = Modifier.fillMaxWidth(),
            singleLine = true
        )

        // Placeholder for EEP Selection Dropdown
        OutlinedTextField(
            value = selectedEep,
            onValueChange = { /* selectedEep = it */ },
            label = { Text("EEP Selection (Dropdown)") },
            modifier = Modifier.fillMaxWidth(),
            readOnly = true,
            singleLine = true
        )

        // Placeholder for Analysis Depth Dropdown
        OutlinedTextField(
            value = analysisDepth,
            onValueChange = { /* analysisDepth = it */ },
            label = { Text("Analysis Depth (Dropdown)") },
            modifier = Modifier.fillMaxWidth(),
            readOnly = true,
            singleLine = true
        )

        // Mathematical Engine Dropdown
        ExposedDropdownMenuBox(
            expanded = engineDropdownExpanded,
            onExpandedChange = { engineDropdownExpanded = !engineDropdownExpanded },
            modifier = Modifier.fillMaxWidth()
        ) {
            OutlinedTextField(
                value = selectedEngine?.displayName ?: "Select Engine", // Handle null case
                onValueChange = {},
                label = { Text("Mathematical Engine") },
                readOnly = true,
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = engineDropdownExpanded) },
                modifier = Modifier.menuAnchor().fillMaxWidth() // Important: menuAnchor
            )
            ExposedDropdownMenu(
                expanded = engineDropdownExpanded,
                onDismissRequest = { engineDropdownExpanded = false }
            ) {
                engineOptions.forEach { option ->
                    when (option) {
                        is EngineOption.Header -> {
                            Text(
                                text = option.title,
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.primary, // Make header stand out
                                modifier = Modifier.padding(start = 16.dp, end = 16.dp, top = 10.dp, bottom = 4.dp)
                            )
                            HorizontalDivider(modifier = Modifier.padding(horizontal = 8.dp, vertical = 4.dp))
                        }
                        is EngineOption.SubHeader -> {
                            Text(
                                text = option.title,
                                style = MaterialTheme.typography.bodySmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                                modifier = Modifier.padding(start = 24.dp, top = 8.dp, bottom = 4.dp, end = 16.dp)
                            )
                        }
                        is EngineOption.Item -> {
                            DropdownMenuItem(
                                text = { Text(option.displayName) },
                                onClick = {
                                    selectedEngine = option
                                    engineDropdownExpanded = false
                                    println("Selected engine: ${option.displayName}")
                                },
                                enabled = option.enabled
                            )
                        }
                    }
                }
            }
        }


        Button(
            onClick = {
                isLoading = true
                println("Analyze clicked: Phenomenon='${phenomenonText}', EEP='${selectedEep}', Depth='${analysisDepth}', Engine='${selectedEngine?.id}'")
                // Simulate loading
                // kotlinx.coroutines.GlobalScope.launch { kotlinx.coroutines.delay(2000); isLoading = false }
            },
            modifier = Modifier.align(Alignment.End).padding(top = 8.dp)
        ) {
            Text("Analyze")
        }

        if (isLoading) {
            LinearProgressIndicator(modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
        }
    }
}

@Composable
fun ResultsDashboard(modifier: Modifier = Modifier) {
    Box(
        modifier = modifier
            .padding(8.dp)
            .background(MaterialTheme.colorScheme.surface.copy(alpha = 0.5f)), // Adjusted background
        contentAlignment = Alignment.Center
    ) {
        Text("Results Dashboard", style = MaterialTheme.typography.titleMedium)
    }
}

@Composable
fun StatusBar(modifier: Modifier = Modifier) {
    Row(
        modifier = modifier
            .padding(horizontal = 16.dp, vertical = 8.dp)
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        Text("Status: Ready", style = MaterialTheme.typography.bodySmall)
        Text("Event ID: None", style = MaterialTheme.typography.bodySmall)
        Text("Time: 0.00s", style = MaterialTheme.typography.bodySmall)
    }
}