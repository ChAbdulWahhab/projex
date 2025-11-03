# Contributing to Projex

First off — thanks for taking the time to contribute! 🎉
Projex is built by developers, for developers, and every improvement helps.

---

## 🧭 How to Contribute

There are several ways you can help improve Projex:

* Report bugs
* Suggest new features or templates
* Improve the documentation
* Fix typos or formatting
* Add tests or improve existing ones
* Enhance the CLI or generation logic

---

## ⚙️ Setting Up Your Development Environment

1. **Fork** the repository on GitHub
   → [https://github.com/ChAbdulWahhab/projex](https://github.com/ChAbdulWahhab/projex)

2. **Clone** your fork locally:

   ```bash
   git clone https://github.com/<your-username>/projex.git
   cd projex
   ```

3. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install development dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Run tests** to make sure everything’s working:

   ```bash
   pytest
   ```

---

## 🧪 Making Changes

* Create a new branch for your feature or bugfix:

  ```bash
  git checkout -b feature/my-new-feature
  ```
* Make your changes with clear, well-structured commits.
* Write or update tests if needed.
* Update documentation if you introduce new behavior.

---

## 🧰 Code Style

Projex follows standard Python formatting and best practices:

* Use **Black** for code formatting
* Use **isort** for import sorting
* Run **flake8** to catch linting issues

You can run them all with:

```bash
black projex
isort projex
flake8 projex
```

---

## 🧾 Commit Messages

Keep commits clear and descriptive. Example:

```
feat: add Docker configuration for Django template
fix: correct typo in FastAPI route
docs: update README setup instructions
```

---

## 🚀 Submitting a Pull Request

1. Push your branch:

   ```bash
   git push origin feature/my-new-feature
   ```
2. Go to your fork on GitHub and open a Pull Request against `main`.
3. Describe **what you changed**, **why**, and **how to test it**.
4. Wait for review and make adjustments if requested.

---

## 🧱 Project Structure

```
projex/
├── cli/                # CLI entry point and commands
├── templates/          # Project templates (FastAPI, Django, Flask, etc.)
├── utils/              # Helper functions and core logic
├── tests/              # Unit and integration tests
├── setup.py
├── requirements.txt
└── README.md
```

---

## 🧠 Tips for Contributors

* Keep PRs small and focused.
* Always sync your fork before starting new work:

  ```bash
  git pull upstream main
  ```
* Use clear variable names and comments where logic isn’t obvious.
* Test generated projects before submitting changes to templates.

---

## 💬 Need Help?

Open a discussion or issue on GitHub:
👉 [https://github.com/ChAbdulWahhab/projex/discussions](https://github.com/ChAbdulWahhab/projex/discussions)

---

**Thank you for helping make Projex better! ❤️**