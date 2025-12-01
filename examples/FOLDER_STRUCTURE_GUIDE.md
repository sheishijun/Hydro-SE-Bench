# Examples Folder Structure Guide

## How to Move Files to a New Folder

### Method 1: Using Git Commands (Recommended)

This method preserves file history in Git.

#### Step 1: Create the folder (if not exists)

The `scripts` folder has been created with a `.gitkeep` file.

#### Step 2: Move files using Git

```powershell
cd "C:\Users\15398\Desktop\test\github V1\hydrosebench-package\examples"

# Move example Python files to scripts folder
git mv example_0_download_data.py scripts/
git mv example_1_basic_evaluation.py scripts/
git mv example_2_batch_evaluation.py scripts/
git mv example_3_custom_benchmark.py scripts/
git mv example_4_sampling.py scripts/
git mv example_5_complete_workflow.py scripts/
```

#### Step 3: Commit the changes

```powershell
git commit -m "Reorganize: Move example scripts to scripts/ folder"
```

#### Step 4: Push to GitHub

```powershell
git push origin main
```

---

### Method 2: Using File System (Alternative)

If you prefer to use file system operations:

#### Step 1: Move files manually

In PowerShell:

```powershell
cd "C:\Users\15398\Desktop\test\github V1\hydrosebench-package\examples"

Move-Item example_0_download_data.py scripts/
Move-Item example_1_basic_evaluation.py scripts/
Move-Item example_2_batch_evaluation.py scripts/
Move-Item example_3_custom_benchmark.py scripts/
Move-Item example_4_sampling.py scripts/
Move-Item example_5_complete_workflow.py scripts/
```

Or move all example files at once:

```powershell
Move-Item example_*.py scripts/
```

#### Step 2: Add to Git

```powershell
git add scripts/
git add -u  # Update tracked files that were moved
```

#### Step 3: Commit and push

```powershell
git commit -m "Reorganize: Move example scripts to scripts/ folder"
git push origin main
```

---

## Notes

- **`.gitkeep` file**: This file is used to keep empty directories in Git (Git doesn't track empty folders)
- **File history**: Using `git mv` preserves file history; using file system moves requires Git to detect the moves
- **Update imports**: If any files import from these moved scripts, you'll need to update the import paths

---

## Suggested Folder Structure

After moving files, your structure might look like:

```
examples/
├── scripts/           # Example Python scripts
│   ├── .gitkeep
│   ├── example_0_download_data.py
│   ├── example_1_basic_evaluation.py
│   ├── example_2_batch_evaluation.py
│   ├── example_3_custom_benchmark.py
│   ├── example_4_sampling.py
│   └── example_5_complete_workflow.py
├── output/           # Output files (example results)
├── README.md         # Documentation
├── test.csv          # Test data
└── utils.py          # Utility functions
```


