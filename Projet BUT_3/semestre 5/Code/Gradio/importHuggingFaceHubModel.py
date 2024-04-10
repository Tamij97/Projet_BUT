# Author : ZHAN Pascal
# Date 09/03/2025
# Project: SAE-GPT2 | BUT 3 Informatique - Semester 5

"""
https://github.com/huggingface/huggingface_hub/blob/main/src/huggingface_hub/keras_mixin.py#L397
It seems the function 'from_pretrained_keras' from Hugging Face's 'huggingface_hub' is not working.
Let's rewrite the code to fix it locally.

To load the model, it's using 'tf.keras.models.load_model', but it's providing a folder instead of the path to the model file
So, we'll search for the first file with the .keras extension in the folder. If None is found then it will raise an error.
"""

from huggingface_hub import ModelHubMixin, snapshot_download
import os
from huggingface_hub.utils import (
    get_tf_version,
    is_tf_available,
)

def from_pretrained_keras(*args, **kwargs) -> "KerasModelHubMixin":
    r"""
    Instantiate a pretrained Keras model from a pre-trained model from the Hub.
    The model is expected to be in `SavedModel` format.
    Args:
        pretrained_model_name_or_path (`str` or `os.PathLike`):
            Can be either:
                - A string, the `model id` of a pretrained model hosted inside a
                  model repo on huggingface.co. Valid model ids can be located
                  at the root-level, like `bert-base-uncased`, or namespaced
                  under a user or organization name, like
                  `dbmdz/bert-base-german-cased`.
                - You can add `revision` by appending `@` at the end of model_id
                  simply like this: `dbmdz/bert-base-german-cased@main` Revision
                  is the specific model version to use. It can be a branch name,
                  a tag name, or a commit id, since we use a git-based system
                  for storing models and other artifacts on huggingface.co, so
                  `revision` can be any identifier allowed by git.
                - A path to a `directory` containing model weights saved using
                  [`~transformers.PreTrainedModel.save_pretrained`], e.g.,
                  `./my_model_directory/`.
                - `None` if you are both providing the configuration and state
                  dictionary (resp. with keyword arguments `config` and
                  `state_dict`).
        force_download (`bool`, *optional*, defaults to `False`):
            Whether to force the (re-)download of the model weights and
            configuration files, overriding the cached versions if they exist.
        resume_download (`bool`, *optional*, defaults to `False`):
            Whether to delete incompletely received files. Will attempt to
            resume the download if such a file exists.
        proxies (`Dict[str, str]`, *optional*):
            A dictionary of proxy servers to use by protocol or endpoint, e.g.,
            `{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}`. The
            proxies are used on each request.
        token (`str` or `bool`, *optional*):
            The token to use as HTTP bearer authorization for remote files. If
            `True`, will use the token generated when running `transformers-cli
            login` (stored in `~/.huggingface`).
        cache_dir (`Union[str, os.PathLike]`, *optional*):
            Path to a directory in which a downloaded pretrained model
            configuration should be cached if the standard cache should not be
            used.
        local_files_only(`bool`, *optional*, defaults to `False`):
            Whether to only look at local files (i.e., do not try to download
            the model).
        model_kwargs (`Dict`, *optional*):
            model_kwargs will be passed to the model during initialization
    <Tip>
    Passing `token=True` is required when you want to use a private
    model.
    </Tip>
    """
    return KerasModelHubMixin.from_pretrained(*args, **kwargs)


class KerasModelHubMixin(ModelHubMixin):
    """
    Implementation of [`ModelHubMixin`] to provide model Hub upload/download
    capabilities to Keras models.
    ```python
    >>> import tensorflow as tf
    >>> from huggingface_hub import KerasModelHubMixin
    >>> class MyModel(tf.keras.Model, KerasModelHubMixin):
    ...     def __init__(self, **kwargs):
    ...         super().__init__()
    ...         self.config = kwargs.pop("config", None)
    ...         self.dummy_inputs = ...
    ...         self.layer = ...
    ...     def call(self, *args):
    ...         return ...
    >>> # Initialize and compile the model as you normally would
    >>> model = MyModel()
    >>> model.compile(...)
    >>> # Build the graph by training it or passing dummy inputs
    >>> _ = model(model.dummy_inputs)
    >>> # Save model weights to local directory
    >>> model.save_pretrained("my-awesome-model")
    >>> # Push model weights to the Hub
    >>> model.push_to_hub("my-awesome-model")
    >>> # Download and initialize weights from the Hub
    >>> model = MyModel.from_pretrained("username/super-cool-model")
    ```
    """

    @classmethod
    def _from_pretrained(
        cls,
        model_id,
        revision,
        cache_dir,
        force_download,
        proxies,
        resume_download,
        local_files_only,
        token,
        **model_kwargs,
    ):
        """Here we just call [`from_pretrained_keras`] function so both the mixin and
        functional APIs stay in sync.
                TODO - Some args above aren't used since we are calling
                snapshot_download instead of hf_hub_download.
        """
        if is_tf_available():
            import tensorflow as tf
        else:
            raise ImportError("Called a TensorFlow-specific function but could not import it.")

        # TODO - Figure out what to do about these config values. Config is not going to be needed to load model
        cfg = model_kwargs.pop("config", None)

        # Root is either a local filepath matching model_id or a cached snapshot
        if not os.path.isdir(model_id):
            storage_folder = snapshot_download(
                repo_id=model_id,
                revision=revision,
                cache_dir=cache_dir,
                library_name="keras",
                library_version=get_tf_version(),
            )
        else:
            storage_folder = model_id

        files = os.listdir(storage_folder)
        modelFileName = None
        nbModel = 0
        for file in files :
          if file.endswith(".keras"):
            modelFileName = file
            nbModel +=1
        
        if modelFileName==None:
          raise ValueError("Repository does not have model that ends with .keras!!!")

        if nbModel > 1:
          raise ValueError("Too many models!!!")

        modelPath = storage_folder + '/' + modelFileName

        model = tf.keras.models.load_model(modelPath, **model_kwargs)

        # For now, we add a new attribute, config, to store the config loaded from the hub/a local dir.
        model.config = cfg
        
        return model
